"""
testhelper/data
---------------

Provides code for interacting with large data during tests.
"""

from io import StringIO
import os

_test_data_dir = os.path.join(os.path.dirname(__file__), "..", "data")


def load_test_data(path: str) -> str:
    """
    Returns the test data in the file at ``path``.

    :param path: path to the test data file relative to ``tests/data``
    """
    sio = StringIO()
    full_path = os.path.join(_test_data_dir, path)
    with open(full_path, "r") as f:
        for ln in f.readlines():
            # Our data files can have lines that start with "#",
            # representing a comment line. Comment lines are
            # discarded from the data.
            if not ln.startswith("#"):
                sio.write(ln)
    val = sio.getvalue()
    sio.close()
    return val
