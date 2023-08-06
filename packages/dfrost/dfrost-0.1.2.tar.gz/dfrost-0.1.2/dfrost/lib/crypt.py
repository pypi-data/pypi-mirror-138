from dfrost.lib.config import get_encryption_key
from dfrost.lib.log import debug
from itertools import count
from struct import pack, unpack
from base64 import urlsafe_b64decode, urlsafe_b64encode


def get_endian():
    return "big"


def get_chunk_size():
    return 64 * 1024 * 1024


def encrypt_file(src, dst):
    fernet = get_encryption_key()
    with open(src, "rb") as src_f:
        with open(dst, "wb") as dst_f:
            for ix in count():
                byte_data = src_f.read(get_chunk_size())
                if byte_data == b"":
                    break
                debug(f"Encrypting file: {src}, chunk: {ix}, writing to: {dst}")
                encrypted = fernet.encrypt(byte_data)
                decoded = urlsafe_b64decode(encrypted)
                dst_f.write(len(decoded).to_bytes(4, get_endian()))
                dst_f.write(decoded)


def decrypt_file(src, dst):
    fernet = get_encryption_key()
    with open(src, "rb") as src_f:
        with open(dst, "wb") as dst_f:
            for ix in count():
                chunk_size = src_f.read(4)
                if chunk_size == b"":
                    break
                debug(f"Decrypting file: {src}, chunk: {ix}, writing to: {dst}")
                to_read = int.from_bytes(chunk_size, get_endian())
                byte_data = src_f.read(to_read)
                encoded = urlsafe_b64encode(byte_data)
                decrypted = fernet.decrypt(encoded)
                dst_f.write(decrypted)
