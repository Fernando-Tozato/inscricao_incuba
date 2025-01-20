import logging
from cryptography.fernet import Fernet
from .settings import SECRET_KEY

class EncryptedFileHandler(logging.FileHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            cipher = Fernet(SECRET_KEY)
            encrypted_msg = cipher.encrypt(msg.encode('utf-8')).decode()
            super().emit(logging.LogRecord(record.name, record.levelno, record.pathname,
                                           record.lineno, encrypted_msg, record.args, record.exc_info))
        except Exception as e:
            print(f"Erro ao criptografar log: {e}")

