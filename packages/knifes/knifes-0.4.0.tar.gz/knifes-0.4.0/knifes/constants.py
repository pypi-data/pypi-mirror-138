from enum import Enum


class MediaType(Enum):
    VIDEO = 'video'
    AUDIO = 'audio'
    IMAGE = 'image'

    def __str__(self):
        """
        Use value when cast to str
        """
        return str(self.value)


APPLE_VERIFY_RECEIPT_PROD = 'https://buy.itunes.apple.com/verifyReceipt'
APPLE_VERIFY_RECEIPT_SANDBOX = 'https://sandbox.itunes.apple.com/verifyReceipt'
ALIPAY_SERVER_URL = 'https://openapi.alipay.com/gateway.do'
