from os.path import expanduser
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from cryptography.fernet import Fernet
from json import loads
from functools import cache


@cache
def get_frost_config():
    with open(expanduser("~/.dfrost.json")) as f:
        return loads(f.read())


def get_storage_bucket():
    return get_frost_config()["storage_bucket"]


def get_encryption_key():
    return Fernet(get_frost_config()["encryption_key"].encode("utf-8"))


def get_sync_dir():
    return get_frost_config()["sync_dir"]


@cache
def get_request_list():
    lines = get_frost_config().get("request_list", list())
    return PathSpec.from_lines(GitWildMatchPattern, lines)


@cache
def get_publish_list():
    lines = get_frost_config().get("publish_list", list())
    return PathSpec.from_lines(GitWildMatchPattern, lines)
