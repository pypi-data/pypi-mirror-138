from dfrost.lib.config import get_encryption_key
from dfrost.lib.log import debug


def get_chunk_size():
    return 64 * 1024 * 1024


def encrypt_file(src, dst):
    debug(f"Encrypting file: {src} -> {dst}")
    fernet = get_encryption_key()
    with open(src, "rb") as src_f:
        with open(dst, "wb") as dst_f:
            while True:
                byte_data = src_f.read(get_chunk_size())
                if byte_data == b"":
                    break
                dst_f.write(fernet.encrypt(byte_data))


def decrypt_file(src, dst):
    debug(f"Decrypting file: {src} -> {dst}")
    fernet = get_encryption_key()
    with open(src, "rb") as src_f:
        with open(dst, "wb") as dst_f:
            while True:
                byte_data = src_f.read(get_chunk_size())
                if byte_data == b"":
                    break
                dst_f.write(fernet.decrypt(byte_data))
