import logging
from cryptography.fernet import Fernet
from .settings import LOGGER_SECRET_KEY

class EncryptedFileHandler(logging.FileHandler):
    def __init__(self, filename, *args, **kwargs):
        super(EncryptedFileHandler, self).__init__(filename, *args, **kwargs)
        self.cipher = Fernet(LOGGER_SECRET_KEY)

    def emit(self, record):
        try:
            msg = self.format(record)
            encrypted_msg = self.cipher.encrypt(msg.encode('utf-8')).decode()
            super().emit(logging.LogRecord(
                record.name, record.levelno, record.pathname, record.lineno,
                encrypted_msg, record.args, record.exc_info
            ))
        except Exception as e:
            print(f"Erro ao criptografar log: {e}")


