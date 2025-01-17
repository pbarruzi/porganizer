from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings

#  key = Fernet.generate_key()


def encrypt(txt):
    try:
        # convert integer etc to string first
        txt = str(txt)
        # get the key from settings
        # key should be byte
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        # input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text)\
            .decode("ascii")
        return encrypted_text
    except Exception:
        # log the error if any
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(txt):
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")
        return decoded_text
    except Exception:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
