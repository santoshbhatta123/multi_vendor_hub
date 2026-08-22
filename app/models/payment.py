from app import db
from datetime import datetime


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)
    payment_method = db.Column(db.String(20), nullable=False, default='esewa')
    transaction_uuid = db.Column(db.String(255), unique=True, nullable=False)
    transaction_code = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), nullable=False, default='NPR')
    status = db.Column(db.String(20), nullable=False, default='PENDING')
    gateway_response = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order = db.relationship('Order', backref='payments', uselist=False)

    def __repr__(self):
        return f'<Payment {self.transaction_uuid} - Rs. {self.amount} - {self.status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'payment_method': self.payment_method,
            'transaction_uuid': self.transaction_uuid,
            'transaction_code': self.transaction_code,
            'amount': float(self.amount),
            'currency': self.currency,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class PaymentLog(db.Model):
    __tablename__ = 'payment_logs'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)
    esewa_response = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    payment = db.relationship('Payment', backref='logs')

    def __repr__(self):
        return f'<PaymentLog {self.id} - {self.status}>'
