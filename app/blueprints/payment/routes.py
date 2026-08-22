from flask import Blueprint, render_template, request, current_app, url_for, redirect, flash
from flask_login import login_required, current_user
from app import db, csrf
from app.models.payment import Payment, PaymentLog
from app.models.order import Order
from app.utils.esewa_gateway import ESewaGateway
from app.utils.decorators import customer_required
import uuid

payment_bp = Blueprint('payment', __name__, template_folder='../../templates/customer')

csrf.exempt(payment_bp)


def get_gateway() -> ESewaGateway:
    cfg = current_app.config
    return ESewaGateway(
        product_code=cfg['ESEWA_PRODUCT_CODE'],
        secret_key=cfg['ESEWA_SECRET_KEY'],
        payment_url=cfg['ESEWA_PAYMENT_URL'],
        verify_url=cfg['ESEWA_VERIFY_URL'],
    )


def _owned_order(order_id):
    """Return the order if it belongs to the logged-in customer, else None."""
    order = Order.query.get_or_404(order_id)
    if order.customer.user_id != current_user.id:
        return None
    return order


# ── Payment Method Selection ──────────────────────────────────

@payment_bp.route('/pay/<int:order_id>')
@login_required
@customer_required
def select_method(order_id):
    order = _owned_order(order_id)
    if not order:
        flash('Unauthorized', 'danger')
        return redirect(url_for('customer.orders'))

    if order.payment_status == 'paid':
        flash('Order already paid', 'warning')
        return redirect(url_for('customer.order_detail', id=order.id))

    return render_template('customer/payment_method.html', order=order)


# ── 1. Cash on Delivery ───────────────────────────────────────

@payment_bp.route('/pay/<int:order_id>/cod', methods=['POST'])
@login_required
@customer_required
def pay_cod(order_id):
    order = _owned_order(order_id)
    if not order:
        flash('Unauthorized', 'danger')
        return redirect(url_for('customer.orders'))

    if order.payment_status == 'paid':
        flash('Order already paid', 'warning')
        return redirect(url_for('customer.order_detail', id=order.id))

    transaction_uuid = f"COD-{uuid.uuid4().hex[:12].upper()}"

    payment = Payment(
        order_id=order.id,
        payment_method='cod',
        transaction_uuid=transaction_uuid,
        amount=order.total_amount,
        currency='NPR',
        status='PENDING',
    )
    db.session.add(payment)

    order.payment_status = 'cod_pending'
    order.status = 'confirmed'
    order.transaction_uuid = transaction_uuid
    db.session.commit()

    db.session.add(PaymentLog(payment_id=payment.id, status='PENDING',
                              message='Cash on delivery selected'))
    db.session.commit()

    flash('Order confirmed! Pay cash on delivery.', 'success')
    return redirect(url_for('customer.order_detail', id=order.id))


# ── 2. eSewa ePay V2 (official UAT) ───────────────────────────

@payment_bp.route('/pay/<int:order_id>/esewa', methods=['POST'])
@login_required
@customer_required
def pay_esewa(order_id):
    order = _owned_order(order_id)
    if not order:
        flash('Unauthorized', 'danger')
        return redirect(url_for('customer.orders'))

    if order.payment_status == 'paid':
        flash('Order already paid', 'warning')
        return redirect(url_for('customer.order_detail', id=order.id))

    # Unique transaction UUID per attempt (prevents duplicate processing)
    transaction_uuid = uuid.uuid4().hex

    amount = f"{float(order.total_amount):.2f}"

    payment = Payment(
        order_id=order.id,
        payment_method='esewa',
        transaction_uuid=transaction_uuid,
        amount=order.total_amount,
        currency='NPR',
        status='PENDING',
    )
    db.session.add(payment)

    order.payment_status = 'pending'
    order.transaction_uuid = transaction_uuid
    db.session.commit()

    db.session.add(PaymentLog(payment_id=payment.id, status='PENDING',
                              message='Redirected to eSewa UAT'))
    db.session.commit()

    gateway = get_gateway()
    host = request.host_url.rstrip('/')
    payload = gateway.build_payment_payload(
        amount=amount,
        transaction_uuid=transaction_uuid,
        success_url=f"{host}{url_for('payment.esewa_success')}",
        failure_url=f"{host}{url_for('payment.esewa_failure')}",
    )

    # Redirect customer to the OFFICIAL eSewa UAT payment page
    return gateway.payment_form_html(current_app.config['ESEWA_PAYMENT_URL'], payload)


# ── eSewa Success Callback ────────────────────────────────────

@payment_bp.route('/esewa-success')
def esewa_success():
    data_param = request.args.get('data')
    response = ESewaGateway.parse_callback(data_param)

    if not response:
        return render_template('customer/esewa_failure.html',
                               reason='Invalid or missing payment response.'), 400

    transaction_uuid = response.get('transaction_uuid')
    claimed_status = response.get('status')
    transaction_code = response.get('transaction_code')

    payment = Payment.query.filter_by(transaction_uuid=transaction_uuid).first()
    if not payment:
        return render_template('customer/esewa_failure.html',
                               reason='Payment record not found for this transaction.'), 404

    order = payment.order

    # Duplicate / replay protection
    if payment.status == 'COMPLETE':
        return render_template('customer/esewa_success.html', payment=payment, order=order)

    gateway = get_gateway()

    # 1) Verify the callback signature (proves the data came from eSewa)
    signature_valid = gateway.verify_response_signature(response)

    # 2) Verify server-side via eSewa status API (prevents replay/fraud)
    txn = gateway.verify_transaction(f"{float(payment.amount):.2f}", transaction_uuid)

    verified_complete = (
        signature_valid
        and txn is not None
        and str(txn.get('status', '')).upper() == 'COMPLETE'
        and claimed_status == 'COMPLETE'
        and float(txn.get('total_amount', 0)) == float(payment.amount)
    )

    payment.gateway_response = {'callback': response, 'verification': txn}

    if not verified_complete:
        payment.status = 'FAILED'
        db.session.add(PaymentLog(payment_id=payment.id, status='FAILED',
                                  message='Server-side verification failed',
                                  esewa_response={'callback': response, 'verification': txn}))
        db.session.commit()
        return render_template('customer/esewa_failure.html',
                               reason='Payment could not be verified with eSewa.',
                               payment=payment)

    payment.status = 'COMPLETE'
    payment.transaction_code = transaction_code or txn.get('ref_id')
    if order:
        order.payment_status = 'paid'
        order.status = 'confirmed'

    db.session.add(PaymentLog(payment_id=payment.id, status='COMPLETE',
                              message='Verified and completed',
                              esewa_response={'callback': response, 'verification': txn}))
    db.session.commit()

    return render_template('customer/esewa_success.html', payment=payment, order=order)


# ── eSewa Failure Callback ────────────────────────────────────

@payment_bp.route('/esewa-failure')
def esewa_failure():
    data_param = request.args.get('data')
    response = ESewaGateway.parse_callback(data_param)

    transaction_uuid = (response or {}).get('transaction_uuid')
    payment = Payment.query.filter_by(transaction_uuid=transaction_uuid).first() \
        if transaction_uuid else None

    if payment and payment.status != 'COMPLETE':
        payment.status = 'FAILED'
        payment.gateway_response = {'callback': response}
        db.session.add(PaymentLog(payment_id=payment.id, status='FAILED',
                                  message='Cancelled or failed at eSewa',
                                  esewa_response={'callback': response}))
        db.session.commit()

    return render_template('customer/esewa_failure.html',
                           reason='Payment was cancelled or failed.',
                           payment=payment)
