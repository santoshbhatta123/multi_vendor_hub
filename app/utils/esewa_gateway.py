import base64
import hashlib
import hmac
import json

import requests


class ESewaGateway:
    """
    Official eSewa ePay V2 integration helper.

    Signature (per official docs):
        message  = "total_amount=<amt>,transaction_uuid=<uuid>,product_code=<code>"
        signature = Base64( HMAC-SHA256( secret_key, message ) )
    """

    SIGNED_FIELD_NAMES = 'total_amount,transaction_uuid,product_code'

    def __init__(self, product_code: str, secret_key: str, payment_url: str, verify_url: str):
        self.product_code = product_code
        self.secret_key = secret_key
        self.payment_url = payment_url
        self.verify_url = verify_url

    # ── Signature ────────────────────────────────────────────

    def make_signature(self, total_amount: str, transaction_uuid: str) -> str:
        message = (
            f"total_amount={total_amount},"
            f"transaction_uuid={transaction_uuid},"
            f"product_code={self.product_code}"
        )
        digest = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(digest).decode('utf-8')

    # ── Payment form payload (redirect to eSewa UAT) ─────────

    def build_payment_payload(self, amount: str, transaction_uuid: str,
                              success_url: str, failure_url: str,
                              tax_amount: str = '0',
                              service_charge: str = '0',
                              delivery_charge: str = '0') -> dict:
        total_amount = amount
        return {
            'amount': amount,
            'tax_amount': tax_amount,
            'total_amount': total_amount,
            'transaction_uuid': transaction_uuid,
            'product_code': self.product_code,
            'product_service_charge': service_charge,
            'product_delivery_charge': delivery_charge,
            'success_url': success_url,
            'failure_url': failure_url,
            'signed_field_names': self.SIGNED_FIELD_NAMES,
            'signature': self.make_signature(total_amount, transaction_uuid),
        }

    def payment_form_html(self, endpoint: str, payload: dict) -> str:
        """Auto-submitting form that redirects the customer to eSewa."""
        inputs = '\n'.join(
            f'<input type="hidden" name="{k}" value="{v}"/>'
            for k, v in payload.items()
        )
        return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Redirecting to eSewa...</title></head>
<body style="font-family:Arial;text-align:center;padding-top:80px;">
<h3>Redirecting to eSewa secure payment...</h3>
<p>Please wait, do not refresh.</p>
<form id="esewaForm" method="POST" action="{endpoint}">
{inputs}
</form>
<script>document.getElementById('esewaForm').submit();</script>
</body></html>"""

    # ── Callback response handling ───────────────────────────

    @staticmethod
    def parse_callback(data_param: str) -> dict | None:
        """Decode the base64 JSON returned by eSewa in the ?data= param."""
        if not data_param:
            return None
        try:
            decoded = base64.b64decode(data_param).decode('utf-8')
            return json.loads(decoded)
        except Exception:
            return None

    def verify_response_signature(self, response: dict) -> bool:
        """
        Verify the signature of the base64-decoded callback response.
        Message is built from the fields listed in response['signed_field_names'],
        in that exact order (same HMAC-SHA256-base64 scheme).
        """
        received_sig = response.get('signature')
        field_names = response.get('signed_field_names')
        if not received_sig or not field_names:
            return False
        try:
            message = ','.join(
                f"{name}={response[name]}" for name in field_names.split(',')
            )
        except KeyError:
            return False
        expected = self.make_signature_from_message(message)
        return hmac.compare_digest(expected, str(received_sig))

    def make_signature_from_message(self, message: str) -> str:
        digest = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(digest).decode('utf-8')

    # ── Server-side verification ─────────────────────────────

    def verify_transaction(self, total_amount: str, transaction_uuid: str) -> dict | None:
        """
        GET {verify_url}?product_code=&total_amount=&transaction_uuid=
        Returns the transaction dict or None.
        Official format: total_amount is the plain numeric amount.
        """
        try:
            resp = requests.get(
                self.verify_url,
                params={
                    'product_code': self.product_code,
                    'total_amount': f'{float(total_amount):.2f}',
                    'transaction_uuid': transaction_uuid,
                },
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            return None

        if isinstance(data, list):
            for txn in data:
                if txn.get('transaction_uuid') == transaction_uuid:
                    return txn
        elif isinstance(data, dict):
            if data.get('transaction_uuid') == transaction_uuid:
                return data
        return None
