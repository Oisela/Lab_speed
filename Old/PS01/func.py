import csv
import numpy as np

def load_csv_columns(filepath, col, ignore_header=True):
    with open(filepath, mode='r') as file:
        csv_reader = csv.reader(file)
        column_data = []
        for i, line in enumerate(csv_reader):
            if ignore_header and i == 0:
                continue
            if col < len(line):
                column_data.append(line[col])
        return column_data
    

def calculate_mean_with_errors(data, correction=0, errors=None):
    # data: list of values
    # correction: correction to the mean value
    if errors is None:
        errors = [0 for _ in data]
    mean = sum(data) / len(data) + correction

    # ¨standard deviation
    s = (sum([(value - mean)**2 for value in data]) / (len(data) * (len(data) - 1)))**0.5
    s_s = s / (len(data)**0.5)
    errors.append(s_s)
    error = phytagorreische_addition(errors) 
    return mean, error



def phytagorreische_addition(errors):
    return (sum([error**2 for error in errors]))**0.5