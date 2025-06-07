import csv
from typing import Callable, Dict, List


def read_csv(path: str) -> List[Dict[str, str]]:
    """Read a CSV file and return a list of rows as dictionaries."""
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def filter_rows(data: List[Dict[str, str]], column: str, predicate: Callable[[str], bool]) -> List[Dict[str, str]]:
    """Filter rows based on a predicate applied to a specific column."""
    return [row for row in data if predicate(row.get(column, ""))]


def column_mean(data: List[Dict[str, str]], column: str) -> float:
    """Compute the mean of a numeric column."""
    values = [float(row[column]) for row in data if row.get(column)
              not in (None, "")]
    if not values:
        return 0.0
    return sum(values) / len(values)


def plot_column(data: List[Dict[str, str]], column: str, width: int = 50) -> None:
    """Display a simple ASCII bar plot for values in a column."""
    values = [float(row[column]) for row in data if row.get(column)
              not in (None, "")]
    if not values:
        print("No data to plot")
        return
    max_val = max(values)
    for value in values:
        bar = "#" * int(width * value / max_val)
        print(f"{value:>8.2f} | {bar}")
