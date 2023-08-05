from tempfile import TemporaryDirectory
from os.path import join
from contextlib import contextmanager


@contextmanager
def get_temp_fname():
    with TemporaryDirectory() as tmpdir:
        yield join(tmpdir, "tmp")
