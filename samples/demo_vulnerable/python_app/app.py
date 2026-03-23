from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

KEY_KIND = "RSA"
CERT_PATH = "/etc/ssl/private/server.key"


def load_private_key(pem_data: bytes):
    return serialization.load_pem_private_key(pem_data, password=None)
