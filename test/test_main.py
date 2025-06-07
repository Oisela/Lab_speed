import os
import sys
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from csv_utils import column_mean, read_csv


def test_column_mean() -> None:
    csv_content = "a,b\n1,2\n3,4\n"
    with tempfile.NamedTemporaryFile("w", delete=False) as fh:
        fh.write(csv_content)
        path = fh.name
    try:
        data = read_csv(path)
        assert column_mean(data, "a") == 2.0
        assert column_mean(data, "b") == 3.0
    finally:
        os.remove(path)
