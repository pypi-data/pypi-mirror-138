from odeo.models.payment_gateway import Payment
from odeo.services.base import *


class PaymentGatewayService(BaseService):

    @authenticated
    def get_payment(self, by_payment_id: int = None, by_reference_id: str = None):
        """Get specific payment order detail by its ID or reference ID

        :param by_payment_id: The ID of the payment order detail retrieved
        :param by_reference_id: The reference ID of the payment order detail retrieved
        :rtype: Payment
        """

        assert (by_payment_id is not None) ^ (by_reference_id is not None), \
            'by_payment_id and by_reference_id parameters are mutually exclusive'

        path = f"/pg/v1/payment/{by_payment_id}" if by_payment_id is not None else ''
        path = f"/pg/v1/payment/reference-id/{by_reference_id}" if by_reference_id is not None else path

        return Payment.from_json(self.request('GET', path).json())
