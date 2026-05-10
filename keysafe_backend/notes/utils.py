from cryptography.fernet import Fernet
from django.conf import settings

cipher = Fernet(settings.ENCRYPTION_KEY)

def encrypt_text(text):

    if not text:
        return text

    return cipher.encrypt(text.encode()).decode()

def decrypt_text(encrypted_text):

    if not encrypted_text:
        return encrypted_text

    return cipher.decrypt(encrypted_text.encode()).decode()