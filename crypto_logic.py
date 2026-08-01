import base64

def encrypt_text(msg):
    encoded_msg = msg.strip().encode("utf-8")
    return base64.b64encode(encoded_msg).decode("utf-8")

def decrypt_text(msg):
    if len(msg.strip()) % 4 != 0:
        raise ValueError("Invalid length")
    decoded_msg = msg.strip().encode("utf-8")
    return base64.b64decode(decoded_msg).decode("utf-8")