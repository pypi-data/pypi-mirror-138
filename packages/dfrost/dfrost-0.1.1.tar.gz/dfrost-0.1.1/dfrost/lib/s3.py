import itertools
from boto3 import client
from botocore.exceptions import ClientError
from enum import Enum, auto
from os import utime
from functools import cache
from dfrost.lib.log import debug
from dfrost.lib.config import get_storage_bucket
from dfrost.lib.crypt import decrypt_file, encrypt_file
from dfrost.lib.temp import get_temp_fname


class FileState(Enum):
    archived = auto()
    restoring = auto()
    restored = auto()


class FileStateInvalidError(Exception):
    pass


class FileDoesntExistError(Exception):
    pass


@cache
def get_s3_client():
    return client("s3")


def get_restore_days():
    return 7


def get_file_state(s3_key):
    try:
        debug(f"Checking state of file: {s3_key}")
        headers = get_s3_client().head_object(Bucket=get_storage_bucket(), Key=s3_key)[
            "ResponseMetadata"
        ]["HTTPHeaders"]
    except ClientError as err:
        if err.response["Error"]["Code"] == "404":
            raise FileDoesntExistError()
        raise

    mtime = int(headers["x-amz-meta-mtime"])
    if "x-amz-restore" not in headers:
        return FileState.archived, mtime
    if headers["x-amz-restore"] == 'ongoing-request="true"':
        return FileState.restoring, mtime
    return FileState.restored, mtime


def list_objects():
    for ix in itertools.count():
        debug(f"Fetching remote batch: {ix} of files")
        resp = get_s3_client().list_objects_v2(
            Bucket=get_storage_bucket(),
            **{"ContinuationToken": resp["NextContinuationToken"]} if ix > 0 else {},
        )
        for item in resp.get("Contents", list()):
            yield item["Key"]
        if not resp["IsTruncated"]:
            break


def restore_file(s3_key):
    try:
        debug(f"Restoring file: {s3_key}")
        get_s3_client().restore_object(
            Bucket=get_storage_bucket(),
            Key=s3_key,
            RestoreRequest={"Days": get_restore_days()},
        )
    except ClientError as err:
        if err.response["Error"]["Code"] == "RestoreAlreadyInProgress":
            raise FileStateInvalidError()
        if err.response["Error"]["Code"] == "NoSuchKey":
            raise FileDoesntExistError()
        raise


def upload_file(s3_key, *, file_path, mtime):
    with get_temp_fname() as fname:
        encrypt_file(file_path, fname)
        debug(f"Uploading file: {s3_key} from src: {fname}")
        get_s3_client().upload_file(
            fname,
            get_storage_bucket(),
            s3_key,
            ExtraArgs={
                "StorageClass": "DEEP_ARCHIVE",
                "Metadata": {"MTime": str(mtime)},
            },
        )


def download_file(s3_key, *, file_path, mtime):
    with get_temp_fname() as fname:
        try:
            debug(f"Downloading file: {s3_key} to dest: {fname}")
            get_s3_client().download_file(get_storage_bucket(), s3_key, fname)
        except ClientError as err:
            if err.response["Error"]["Code"] == "404":
                raise FileDoesntExistError()
            if err.response["Error"]["Code"] == "InvalidObjectState":
                raise FileStateInvalidError()
            raise
        decrypt_file(fname, file_path)
        utime(file_path, (mtime, mtime))
