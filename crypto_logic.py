import base64
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

RSA_MAX_MSG_BYTES = 190  # limit for a 2048-bit key using OAEP-SHA256 padding

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




# ---- Caesar Cipher ----

def caesar_encrypt(msg, shift_input):
    try:
        shift = int(shift_input) % 26
    except (ValueError, TypeError):
        raise ValueError("Please enter a valid whole number for the shift.")

    result = []
    for char in msg.strip():
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result.append(chr(base + shifted))
        else:
            result.append(char)
    return "".join(result)

def caesar_decrypt(msg, shift_input):
    try:
        shift = int(shift_input) % 26
    except (ValueError, TypeError):
        raise ValueError("Please enter a valid whole number for the shift.")

    result = []
    for char in msg.strip():
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base - shift) % 26
            result.append(chr(base + shifted))
        else:
            result.append(char)
    return "".join(result)


# ---- XOR Cipher (uses passcode as a repeating key) ----

def xor_encrypt(msg, passcode):
    if passcode == "":
        raise ValueError("A password is required for XOR encryption.")

    msg_bytes = msg.strip().encode("utf-8")
    key_bytes = passcode.encode("utf-8")

    xored = bytearray()
    for i, byte in enumerate(msg_bytes):
        key_byte = key_bytes[i % len(key_bytes)]  # repeat the key as needed
        xored.append(byte ^ key_byte)

    # XOR output is unprintable bytes, so the base64-wrap displays/saves it as text instead
    return base64.b64encode(bytes(xored)).decode("utf-8")

def xor_decrypt(msg, passcode):
    if passcode == "":
        raise ValueError("A password is required for XOR decryption.")

    try:
        xored = base64.b64decode(msg.strip().encode("utf-8"))
    except Exception:
        raise ValueError("Invalid input. Please enter valid encrypted text.")

    key_bytes = passcode.encode("utf-8")

    original = bytearray()
    for i, byte in enumerate(xored):
        key_byte = key_bytes[i % len(key_bytes)]
        original.append(byte ^ key_byte)

    try:
        return original.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Incorrect password, or corrupted text.")



# ---- ChaCha20 ----

def chacha20_encrypt(msg, passcode):
    salt = os.urandom(SALT_SIZE)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000).derive(passcode.encode("utf-8"))
    nonce = os.urandom(12)  # ChaCha20Poly1305 requires a 12-byte nonce
    cipher = ChaCha20Poly1305(key)
    ciphertext = cipher.encrypt(nonce, msg.strip().encode("utf-8"), None)
    combined = salt + nonce + ciphertext
    return base64.urlsafe_b64encode(combined).decode("utf-8")

def chacha20_decrypt(msg, passcode):
    try:
        combined = base64.urlsafe_b64decode(msg.strip().encode("utf-8"))
        salt = combined[:SALT_SIZE]
        nonce = combined[SALT_SIZE:SALT_SIZE + 12]
        ciphertext = combined[SALT_SIZE + 12:]
        key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000).derive(passcode.encode("utf-8"))
        cipher = ChaCha20Poly1305(key)
        result = cipher.decrypt(nonce, ciphertext, None)
        return result.decode("utf-8")
    except Exception:
        raise ValueError("Decryption failed. Wrong password or corrupted text.")


# ---- RSA ----

def rsa_generate_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode("utf-8")

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")

    return public_pem, private_pem

def rsa_encrypt(msg, public_key_pem):
    if not public_key_pem.strip():
        raise ValueError("Please set a public key first (Algorithm > Manage RSA Keys).")

    try:
        public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
    except Exception:
        raise ValueError("Invalid public key format.")

    msg_bytes = msg.strip().encode("utf-8")
    if len(msg_bytes) > RSA_MAX_MSG_BYTES:
        raise ValueError(f"Message too long for RSA (max {RSA_MAX_MSG_BYTES} bytes). Try a shorter message or a different algorithm.")

    ciphertext = public_key.encrypt(
        msg_bytes,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return base64.b64encode(ciphertext).decode("utf-8")

def rsa_decrypt(msg, private_key_pem):
    if not private_key_pem.strip():
        raise ValueError("Please set a private key first (Algorithm > Manage RSA Keys).")

    try:
        private_key = serialization.load_pem_private_key(private_key_pem.encode("utf-8"), password=None)
    except Exception:
        raise ValueError("Invalid private key format.")

    try:
        ciphertext = base64.b64decode(msg.strip().encode("utf-8"))
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        return plaintext.decode("utf-8")
    except Exception:
        raise ValueError("Decryption failed. Wrong key or corrupted text.")










# ---- Registry ----
# Every algorithm here must provide (encrypt_func, decrypt_func)

ALGORITHMS = {
    "AES": (aes_encrypt, aes_decrypt),
    "Base64": (base64_encrypt, base64_decrypt),
    "Caesar": (caesar_encrypt, caesar_decrypt),
    "XOR": (xor_encrypt, xor_decrypt),
    "ChaCha20": (chacha20_encrypt, chacha20_decrypt),
    "RSA": (rsa_encrypt, rsa_decrypt),
}

INPUT_TYPE = {
    "AES": "passcode",
    "Base64": "none",
    "Caesar": "number",
    "XOR": "passcode",
    "ChaCha20": "passcode",
    "RSA": "keypair",
}

DEFAULT_ALGORITHM = "AES"