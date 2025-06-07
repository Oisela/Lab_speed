import argparse

from .csv_utils import column_mean, plot_column, read_csv


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load a CSV file, manipulate data and plot a column.")
    parser.add_argument("file", help="Path to the CSV file")
    parser.add_argument("column", help="Name of the numeric column to analyse")
    args = parser.parse_args()

    data = read_csv(args.file)
    mean = column_mean(data, args.column)
    print(f"Mean of {args.column}: {mean:.2f}")
    print()
    plot_column(data, args.column)


if __name__ == "__main__":
    main()
