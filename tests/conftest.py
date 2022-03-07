import tempfile

import pytest


@pytest.fixture
def input_file():
    input_file = tempfile.NamedTemporaryFile()
    data = b"stuff"
    input_file.write(data)
    input_file.flush()
    input_file.seek(0)
    yield input_file.name, len(data)
    input_file.close()
