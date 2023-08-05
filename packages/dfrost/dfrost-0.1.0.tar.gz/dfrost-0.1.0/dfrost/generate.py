from dfrost.lib.command import register
from cryptography.fernet import Fernet


@register("generate")
def run(args):
    generate()


def generate():
    print(Fernet.generate_key().decode("utf-8"), flush=True)
