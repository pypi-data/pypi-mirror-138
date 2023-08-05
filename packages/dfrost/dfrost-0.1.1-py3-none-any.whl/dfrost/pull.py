from os.path import join, exists, getmtime
from dfrost.lib.s3 import (
    FileDoesntExistError,
    FileState,
    FileStateInvalidError,
    download_file,
    list_objects,
    get_file_state,
    restore_file,
    upload_file,
)
from dfrost.lib.log import info, debug, warn
from dfrost.lib.config import get_request_list, get_sync_dir
from dfrost.lib.command import register


def setup_parser(parser):
    parser.add_argument("--dry-run", action="store_true")


@register("pull", setup_fn=setup_parser)
def run(args):
    pull(dry_run=args.dry_run)


def pull(*, dry_run):
    for s3_key in list_objects():

        if not get_request_list().match_file(s3_key):
            debug(f"File: {s3_key} skipped as it isn't requested.")
            continue

        try:
            state, mtime = get_file_state(s3_key)
            local_path = join(get_sync_dir(), s3_key)
            if exists(local_path) and int(getmtime(local_path)) >= mtime:
                debug(f"Skipping pull of file: {s3_key} as it already exists")
                continue

            if exists(local_path):
                info(f"File: {s3_key} is stale locally and must be pulled")
            else:
                info(f"File: {s3_key} is missing locally and must be pulled")

            if state == FileState.archived:
                info(f"File: {s3_key} is in an archived state and must be restored")
                if not dry_run:
                    restore_file(s3_key)
                continue
            if state == FileState.restoring:
                info(f"File: {s3_key} is in the process of being restored")
                continue
            if state == FileState.restored:
                info(f"File: {s3_key} is ready to be pulled")
                if not dry_run:
                    download_file(s3_key, file_path=local_path, mtime=mtime)

        except FileDoesntExistError:
            warn(f"File: {s3_key} unexpectedly disappeared")
            continue
        except FileStateInvalidError:
            warn(f"File: {s3_key} changed state unexpectedly")
            continue
