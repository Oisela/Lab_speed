import csv
import os
import numpy as np
from datetime import datetime
import math
import pandas as pd
import sys
import importlib.util

def read_csv_data(file_path, delimiter=',', skip_header=True):
    """
    Read data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        delimiter (str): Delimiter used in the CSV file
        skip_header (bool): Whether to skip the header row
        
    Returns:
        np.ndarray: Array containing the data from the CSV file
    """
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        if skip_header:
            next(reader, None)  # Skip the header row
        data = np.array(list(reader), dtype=float)
    return data

def write_to_file(file_path, text):
    """
    Append text to a file.
    
    Args:
        file_path (str): Path to the file
        text (str): Text to append
    """
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(text + '\n')
    except Exception as e:
        print(f"An error occurred: {e}")
        
def create_results_directory(base_dir):
    """
    Create a directory for storing results if it doesn't exist.
    
    Args:
        base_dir (str): Base directory path
        
    Returns:
        str: Path to the results directory
    """
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    return results_dir

def format_scientific_error(number, significant_digits):
    """
    Format a number to scientific notation with a given number of significant digits. 
    Exmaple:
    
    Args:
        number (float): Number to format in a array 
        significant_digits (int): Number of significant digits
        
    Returns:
        str: Formatted number as string
    """


    return number

        

        
def calculate_multimeter_uncertainty(value, uncertainty_percent, resolution, plus_term):
    """
    Calculate the uncertainty of a measurement made with a multimeter.
    
    Args:
        value (float): Measured value
        uncertainty_percent (float): Uncertainty in percentage (e.g., 0.01 for 1%)
        resolution (float): Resolution of the multimeter
        plus_term (int): Plus term integer (e.g., 1 for 0.1)
        
    Returns:
        float: Calculated uncertainty
    """
    # Fix for negative values: use absolute value for percentage calculation
    uncertainty = abs(value) * uncertainty_percent
    additional = resolution * plus_term
    return uncertainty + additional

def get_data_from_csv(data, x_col, y_col, x_err_col, y_err_col):
    """
    Extract data from a csv file.
    """
    x_data = data[x_col].values
    y_data = data[y_col].values
    x_errors = data[x_err_col].values if x_err_col in df.columns else np.zeros_like(x_data)
    y_errors = data[y_err_col].values if y_err_col in df.columns else np.zeros_like(y_data)
    return x_data, y_data, x_errors, y_errors

def load_config(config_path):
    """Dynamically load configuration from a Python file and execute it."""
    with open(config_path, 'r') as file:
        config_code = file.read()
    
    config = {}
    exec(config_code, config)
    
    # Remove built-in keys that get added by exec
    clean_config = {k: v for k, v in config.items() if not k.startswith('__')}
    
    return clean_config

def read_csv_data_pandas(file_path):
    """Read data from CSV file using pandas, detecting headers automatically."""
    try:
        # Use pandas to read CSV file with automatic header detection
        df = pd.read_csv(file_path)
        
        # Print available columns for debugging
        print(f"Columns found in CSV: {list(df.columns)}")
        
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

def save_results(output_filepath, measurement_numbers, results, calc_errors, 
                 variables_dict, result_name, result_unit, significant_digits):
    """Save measurement results to a file."""
    with open(output_filepath, 'a', encoding='utf-8') as f:
        f.write("\n\nMeasurement Results:\n")
        f.write("-------------------\n")
        f.write(f"{'No.':<5} {result_name:<20} {'Error':<20} {'Unit':<10}\n")
        f.write("-" * 55 + "\n")
        
        for i, (result, error) in enumerate(zip(results, calc_errors)):
            f.write(f"{measurement_numbers[i]:<5} {result:<20.{significant_digits}g} "
                   f"{error:<20.{significant_digits}g} {result_unit:<10}\n")
        
        f.write("\n\nVariable Values:\n")
        f.write("---------------\n")
        for var_name, values in variables_dict.items():
            f.write(f"{var_name}: {values}\n")




def save_fit_results(output_filepath, coeffs, coeff_errors, r_squared, significant_digits, unit):
    """Save fit results to a file."""
    with open(output_filepath, 'a', encoding='utf-8') as f:
        f.write("\n\nFit Results:\n")
        f.write("-----------\n")
        f.write(f"R-squared: {r_squared:.{significant_digits}g}\n\n")
        
        f.write(f"{'Parameter':<10} {'Value':<20} {'Error':<20} {'Unit':<10}\n")
        f.write("-" * 60 + "\n")
        
        for i, (coeff, error) in enumerate(zip(coeffs, coeff_errors)):
            if i == 0:
                param_name = "Intercept"
            elif i == 1:
                param_name = "Slope"
            else:
                param_name = f"a{i}"
                
            f.write(f"{param_name:<10} {coeff:<20.{significant_digits}g} "
                   f"{error:<20.{significant_digits}g} {unit:<10}\n")

def prepare_data_from_config(config, base_dir):
    """Extract and prepare data based on configuration."""
    if config['USE_DIRECT_DATA']:
        # Use data defined in config
        if 'x_data' not in config:
            # For backwards compatibility, check if variables exist globally in the module
            print("Warning: Using global data variables from config file")
            x_data = config.get('x_data', [])
            y_data = config.get('y_data', [])
            x_errors = config.get('x_errors', [])
            y_errors = config.get('y_errors', [])
        else:
            x_data = config['x_data']
            y_data = config['y_data']
            x_errors = config['x_errors']
            y_errors = config['y_errors']
            
            # Check if arrays are all the same length
            if not (len(x_data) == len(y_data) == len(x_errors) == len(y_errors)):
                print("Error: Data arrays must be of the same length")
                sys.exit(1)
        
        measurement_numbers = list(range(1, len(x_data) + 1))
        
        # Variables dictionary for output
        variables_dict = {
            'X values': x_data,
            'Y values': y_data,
            'X errors': x_errors,
            'Y errors': y_errors
        }
        
        data_files = {
            'main': {
                'x_data': x_data,
                'y_data': y_data,
                'x_errors': x_errors,
                'y_errors': y_errors,
                'measurement_numbers': measurement_numbers
            }
        }
    else:
        # Read data from CSV file
        csv_path = os.path.join(base_dir, config['DATA_FILE'])
        df = read_csv_data_pandas(csv_path)

        # Set Column names
        if config['AUTO_DETECT_COLUMNS']:
            # Get column names from the detected columns
            x_col = df.columns[0]
            y_col = df.columns[1] if len(df.columns) > 1 else 'Y'
            x_err_col = df.columns[2] if len(df.columns) > 2 else 'X_Error'
            y_err_col = df.columns[3] if len(df.columns) > 3 else 'Y_Error'
        else:
            x_col = config['X_COLUMN']
            y_col = config['Y_COLUMN']
            x_err_col = config['X_ERROR_COLUMN']
            y_err_col = config['Y_ERROR_COLUMN']
        
        # Extract data
        x_data = df[x_col].values
        y_data = df[y_col].values
        x_errors = df[x_err_col].values if x_err_col in df.columns else np.zeros_like(x_data)
        y_errors = df[y_err_col].values if y_err_col in df.columns else np.zeros_like(y_data)
        
        # Create measurement numbers
        measurement_numbers = list(range(1, len(x_data) + 1))
        
        data_files = {
            'main': {
                'x_data': x_data,
                'y_data': y_data,
                'x_errors': x_errors,
                'y_errors': y_errors,
                'measurement_numbers': measurement_numbers
            }
        }
        
        # Read second data file if provided
        if 'DATA_FILE2' in config and config['DATA_FILE2'] != "":
            # Read second data file
            csv_path2 = os.path.join(base_dir, config['DATA_FILE2'])
            df2 = read_csv_data_pandas(csv_path2)
            
            # Extract data from second file
            x_data2 = df2[x_col].values if x_col in df2.columns else df2.iloc[:, 0].values
            y_data2 = df2[y_col].values if y_col in df2.columns else df2.iloc[:, 1].values
            x_errors2 = df2[x_err_col].values if x_err_col in df2.columns else np.zeros_like(x_data2)
            y_errors2 = df2[y_err_col].values if y_err_col in df2.columns else np.zeros_like(y_data2)
            
            # Add to data_files dictionary
            data_files['secondary'] = {
                'x_data': x_data2,
                'y_data': y_data2,
                'x_errors': x_errors2,
                'y_errors': y_errors2,
                'measurement_numbers': list(range(1, len(x_data2) + 1))
            }
        
        # Read third data file if provided
        if 'DATA_FILE3' in config and config['DATA_FILE3'] != "":
            # Read third data file
            csv_path3 = os.path.join(base_dir, config['DATA_FILE3'])
            df3 = read_csv_data_pandas(csv_path3)
            
            # Extract data from third file
            x_data3 = df3[x_col].values if x_col in df3.columns else df3.iloc[:, 0].values
            y_data3 = df3[y_col].values if y_col in df3.columns else df3.iloc[:, 1].values
            x_errors3 = df3[x_err_col].values if x_err_col in df3.columns else np.zeros_like(x_data3)
            y_errors3 = df3[y_err_col].values if y_err_col in df3.columns else np.zeros_like(y_data3)
            
            # Add to data_files dictionary
            data_files['tertiary'] = {
                'x_data': x_data3,
                'y_data': y_data3,
                'x_errors': x_errors3,
                'y_errors': y_errors3,
                'measurement_numbers': list(range(1, len(x_data3) + 1))
            }
        
        # Variables dictionary for output - using main data
        variables_dict = {
            'X values': x_data,
            'Y values': y_data,
            'X errors': x_errors,
            'Y errors': y_errors
        }
    
    return data_files, variables_dict



def prepare_example_data():
    """Prepare data from example data defined in the program."""
    data_sets = {}
    variables_dict = {}
    
    # Process main dataset (dataset1)
    main_dataset = EXAMPLE_DATA["dataset1"]
    x_data = np.array(main_dataset["x_data"])
    y_data = np.array(main_dataset["y_data"])
    x_errors = np.array(main_dataset["x_errors"])
    y_errors = np.array(main_dataset["y_errors"])
    
    # Create measurement numbers
    measurement_numbers = list(range(1, len(x_data) + 1))
    
    # Add to data_sets dictionary
    data_sets['main'] = {
        'x_data': x_data,
        'y_data': y_data,
        'x_errors': x_errors,
        'y_errors': y_errors,
        'measurement_numbers': measurement_numbers,
        'file_name': "Example Dataset 1"
    }
    
    # Store variables for first dataset
    variables_dict = {
        'X values': x_data,
        'Y values': y_data,
        'X errors': x_errors,
        'Y errors': y_errors
    }
    
    # Process additional datasets
    dataset_counter = 1
    for key, dataset in EXAMPLE_DATA.items():
        if key != "dataset1":  # Skip main dataset as it's already processed
            dataset_x_data = np.array(dataset["x_data"])
            dataset_y_data = np.array(dataset["y_data"])
            dataset_x_errors = np.array(dataset["x_errors"])
            dataset_y_errors = np.array(dataset["y_errors"])
            
            # Create measurement numbers
            dataset_measurement_numbers = list(range(1, len(dataset_x_data) + 1))
            
            # Add to data_sets dictionary
            dataset_key = f'dataset_{dataset_counter}'
            data_sets[dataset_key] = {
                'x_data': dataset_x_data,
                'y_data': dataset_y_data,
                'x_errors': dataset_x_errors,
                'y_errors': dataset_y_errors,
                'measurement_numbers': dataset_measurement_numbers,
                'file_name': f"Example Dataset {dataset_counter + 1}"
            }
            dataset_counter += 1
    
    return data_sets, variables_dict