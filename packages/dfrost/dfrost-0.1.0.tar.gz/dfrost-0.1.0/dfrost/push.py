from os.path import join, getmtime, relpath
from os import walk
from cryptography.fernet import Fernet

from dfrost.lib.s3 import (
    FileDoesntExistError,
    get_file_state,
    upload_file,
)
from dfrost.lib.log import info, debug
from dfrost.lib.config import get_publish_list, get_sync_dir
from dfrost.lib.command import register


def setup_parser(parser):
    parser.add_argument("--dry-run", action="store_true")


@register("push", setup_fn=setup_parser)
def run(args):
    push(dry_run=args.dry_run)


def push(*, dry_run):
    for dirname, dirs, files in walk(get_sync_dir()):
        for fname in files:
            local_path = join(dirname, fname)
            s3_key = relpath(local_path, get_sync_dir())

            if not get_publish_list().match_file(s3_key):
                debug(f"File: {s3_key} skipped as it isn't published.")
                continue

            local_mtime = int(getmtime(local_path))

            try:
                state, mtime = get_file_state(s3_key)
                if local_mtime <= mtime:
                    debug(f"Skipping push of file: {s3_key} as it already exists")
                    continue
                info(f"File: {s3_key} is stale remotely and must be pushed")
                if not dry_run:
                    upload_file(s3_key, file_path=local_path, mtime=local_mtime)

            except FileDoesntExistError:
                info(f"File: {s3_key} is missing remotely and must be pushed")
                if not dry_run:
                    upload_file(s3_key, file_path=local_path, mtime=local_mtime)
