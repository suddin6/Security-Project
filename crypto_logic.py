import base64
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_SIZE = 16


# ---- AES ----

def _derive_key(passcode, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000)
    key = kdf.derive(passcode.encode("utf-8"))
    return base64.urlsafe_b64encode(key)

def aes_encrypt(msg, passcode):
    salt = os.urandom(SALT_SIZE)
    key = _derive_key(passcode, salt)
    token = Fernet(key).encrypt(msg.strip().encode("utf-8"))
    combined = salt + token
    return base64.urlsafe_b64encode(combined).decode("utf-8")

def aes_decrypt(msg, passcode):
    try:
        combined = base64.urlsafe_b64decode(msg.strip().encode("utf-8"))
        salt = combined[:SALT_SIZE]
        token = combined[SALT_SIZE:]
        key = _derive_key(passcode, salt)
        result = Fernet(key).decrypt(token)
        return result.decode("utf-8")
    except Exception:
        raise ValueError("Decryption failed. Wrong password or corrupted text.")


# ---- Base64 (encoding only) ----

def base64_encrypt(msg, passcode):
    return base64.b64encode(msg.strip().encode("utf-8")).decode("utf-8")

def base64_decrypt(msg, passcode):
    try:
        if len(msg.strip()) % 4 != 0:
            raise ValueError()
        return base64.b64decode(msg.strip().encode("utf-8")).decode("utf-8")
    except Exception:
        raise ValueError("Invalid input. Please enter a valid encoded text.")


# ---- Registry ----
# Every algorithm here must provide (encrypt_func, decrypt_func) with signature (msg, passcode) -> str

ALGORITHMS = {
    "AES": (aes_encrypt, aes_decrypt),
    "Base64": (base64_encrypt, base64_decrypt),
}

DEFAULT_ALGORITHM = "AES"