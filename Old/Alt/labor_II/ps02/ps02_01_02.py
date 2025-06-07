#!/usr/bin/env python3
"""
Physics Lab Data Analysis Script

Usage:
    Run with: python ps02.py
    
    Results are saved in a 'results' directory in the same location as this program.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import ast
import scipy
from scipy import constants as const

# Add parent directory to sys.path to import package
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)

# Import lab tools package
from pylab import *
from pylab.utils import *
from calculation import *
from pylab.output import *
from pylab.plotting import *

def get_results_directory(RESULTS_DIRECTORY):
    """Create and return the results directory."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the results directory based on configuration or default
    if RESULTS_DIRECTORY is not None:
        # If RESULTS_DIRECTORY is an absolute path, use it directly
        if os.path.isabs(RESULTS_DIRECTORY):
            results_dir = RESULTS_DIRECTORY
        else:
            # Otherwise, make it relative to the script directory
            results_dir = os.path.join(script_dir, RESULTS_DIRECTORY)
    else:
        # Use default 'results' directory in script directory
        results_dir = os.path.join(script_dir, "results")
    
    # Ensure the directory exists
    os.makedirs(results_dir, exist_ok=True)
    return results_dir

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
        'file_name': "Dataset 1"
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
                'file_name': f"Dataset {dataset_counter + 1}"
            }
            dataset_counter += 1
    
    return data_sets, variables_dict

# ===== CONFIGURATION VARIABLES =====
EXPERIMENT_NAME = "Boyle-Mariottesches Gesetz"
RESULTS_DIRECTORY = None  # Custom directory for results (relative to script location or absolute path)
                         # None means use 'results' in the same directory as this script

# Get results directory using the program's location
results_dir = get_results_directory(RESULTS_DIRECTORY)
output_filename = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
output_filepath = os.path.join(results_dir, output_filename)

# Initialize output file
with open(output_filepath, 'w', encoding='utf-8') as f:
    f.write(f"Analysis Results for {EXPERIMENT_NAME}\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"Using example data defined in the program\n\n")



h = [ 13.3, 13, 12.8, 12.5, 12.3]

temp = [44, 34, 31, 23, 18]

h = [25.5,24,21.4,20.2,19.1,17.4,16.6,15.1,14,13,11.9,11]
p_0 = 996
p_Hg = 13.6e3 * const.g * 1.2e-2
Q = np.pi * (0.27)**2 / 4

print(p_Hg)
print(const.g)
save_result(output_filepath, ["Q"], [Q], ["0"], ["cm^2"])

p = []
V = []

p_2 = []

for dp in delta_p_2:
    x = p_0 + dp + p_Hg/100
    p_2.append(x)

for dp in delta_p: 
    x = p_0 + dp + p_Hg/100
    p.append(x)
for vol in h:
    x = vol * Q
    V.append(x)

x_errors = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
y_errors = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]

a = [20] * 12

EXAMPLE_DATA = {

    "dataset1": {
        "x_data": V,
        "y_data": p,
        "x_errors": x_errors,
        "y_errors": y_errors
    },
    "Barometer": {
        "x_data": V,
        "y_data": p_2,
        "x_errors": x_errors,
        "y_errors": y_errors
    }
}

print(h)


# Results configuration
RESULTS_DIRECTORY = None  # Custom directory for results (relative to script location or absolute path)
                         # None means use 'results' in the same directory as this script

# Analysis configuration
FORMULA = "y"         # Formula to calculate results
VARIABLES = "y x a"         # Variables in formula (space-separated)
SCALING_FACTOR = 1.0      # Scaling factor for results
SIGNIFICANT_DIGITS = 3    # Number of significant digits for results
CALCULATE_WEIGHTED_MEAN = True  # Calculate weighted mean of results

# Result information
RESULT_NAME = "se"    # Name of the calculated result
RESULT_UNIT = "m/s"       # Unit of the calculated result

# Plotting configuration
PLOT_ENABLED = True       # Enable/disable plotting
PLOT_TITLE = "Boyle-Mariotte’sches Gesetz"  # Plot title (None = auto-generate)
PLOT_XLABEL = r"Volumen ($cm^3$)"  # X-axis label (None = auto-generate)
PLOT_YLABEL = "Druck (mbar)"  # Y-axis label (None = auto-generate)
PLOT_STYLE = "ro"         # Plot style for data points
PLOT_SHOW_ERRORS = False   # Show error bars
PLOT_X_MIN = None         # Minimum value for x-axis (None for auto)
PLOT_X_MAX = None         # Maximum value for x-axis (None for auto)
PLOT_Y_MIN = None         # Minimum value for y-axis (None for auto)
PLOT_Y_MAX = None         # Maximum value for y-axis (None for auto)

# Fitting configuration
FIT_ENABLED = True       # Enable/disable fitting
FIT_TYPE = "polynomial"   # "polynomial" or "custom"
FIT_DEGREE = 2            # Degree of polynomial fit (if FIT_TYPE is "polynomial")
FIT_FUNCTION = "lambda x: 1/x"      # Custom fit function (if FIT_TYPE is "custom") as string e.g., "lambda x, a, b: a * x + b"
FIT_INITIAL_GUESS = [1, 0]  # Initial guess for parameters (if FIT_TYPE is "custom")
FIT_STYLE = "b-"          # Plot style for fit line
FIT_LABEL = r"Fit for Dataset 1"  # Label for fit line

# ===== END OF CONFIGURATION =====



def main():
    """Main analysis function"""
    print(f"Starting analysis for: {EXPERIMENT_NAME}")
    
    # Prepare data from example data
    data_sets, variables_dict = prepare_example_data()
    
    # Process main data
    main_data = data_sets['main']
    x_data = main_data['x_data']
    y_data = main_data['y_data']
    x_errors = main_data['x_errors']
    y_errors = main_data['y_errors']
    measurement_numbers = main_data['measurement_numbers']
    
    # Create measurements and errors arrays for calculation
    measurements = []
    errors = [] 
    
    # Extract data for calculation
    variables = VARIABLES.split()
    if 'x' in variables and 'y' in variables:
        for i in range(len(x_data)):
            # Order matters! Ensure this matches the order in variables
            measurements.append([y_data[i], x_data[i]])
            errors.append([y_errors[i], x_errors[i]])
    
    # Calculate results and errors
    num_measurements = len(measurements)
    results, calc_errors = calculate_results_with_errors(
        num_measurements,
        SCALING_FACTOR,
        FORMULA,
        VARIABLES,
        measurements,
        errors
    )
    
    # Process other datasets if available
    additional_datasets = {}
    for key, dataset in data_sets.items():
        if key != 'main':
            dataset_x_data = dataset['x_data']
            dataset_y_data = dataset['y_data']
            dataset_x_errors = dataset['x_errors']
            dataset_y_errors = dataset['y_errors']
            
            # Create measurements and errors arrays
            dataset_measurements = []
            dataset_errors = []
            for i in range(len(dataset_x_data)):
                dataset_measurements.append([dataset_y_data[i], dataset_x_data[i]])
                dataset_errors.append([dataset_y_errors[i], dataset_x_errors[i]])
            
            num_measurements = len(dataset_measurements)
            dataset_results, dataset_calc_errors = calculate_results_with_errors(
                num_measurements,
                SCALING_FACTOR,
                FORMULA,
                VARIABLES,
                dataset_measurements,
                dataset_errors
            )
            
            additional_datasets[key] = {
                'x_data': dataset_x_data,
                'results': dataset_results,
                'errors': dataset_calc_errors,
                'label': f"{dataset['file_name']}"
            }
    
    # Calculate weighted mean if enabled
    if CALCULATE_WEIGHTED_MEAN:
        weighted_mean, weighted_mean_error = calculate_weighted_mean(results, calc_errors)
        write_to_file(
            output_filepath,
            f"Weighted Mean: {weighted_mean:.{SIGNIFICANT_DIGITS}g} {RESULT_UNIT}\n" +
            f"Weighted Mean Error: {weighted_mean_error:.{SIGNIFICANT_DIGITS}g} {RESULT_UNIT}\n"
        )
    
    # Create plot if enabled
    if PLOT_ENABLED:
        plt.figure(figsize=(10, 6))
        
        # Plot main data
        plot_y_errors = calc_errors if PLOT_SHOW_ERRORS else None
        
        # Plot data points
        plot_data_with_errors(
            x_data, results, plot_y_errors, None,
            style=PLOT_STYLE,
            label=f"{main_data['file_name']}"
        )
        
        # Plot additional datasets
        plot_styles = ['go', 'bo', 'mo', 'co', 'yo', 'ko']
        for i, (key, dataset) in enumerate(additional_datasets.items()):
            style_index = i % len(plot_styles)
            plot_data_with_errors(
                dataset['x_data'], dataset['results'],
                dataset['errors'] if PLOT_SHOW_ERRORS else None,
                None,
                style=plot_styles[style_index],
                label=dataset['label']
            )
        
        # Add fit if enabled
        if FIT_ENABLED:
            if FIT_TYPE == "custom" and FIT_FUNCTION:
                # Convert string to lambda function
                try:
                    fit_func = eval(FIT_FUNCTION)
                    initial_guess = FIT_INITIAL_GUESS
                    coeffs, coeff_errors, r_squared = generate_fit_data(
                        x_data, results,
                        fit_type="custom",
                        y_errors=plot_y_errors,
                        custom_fit_func=fit_func,
                        initial_guess=initial_guess,
                        style=FIT_STYLE,
                        label=FIT_LABEL
                    )
                except Exception as e:
                    print(f"Error in custom fit function: {e}")
                    print("Falling back to polynomial fit")
                    coeffs, coeff_errors, r_squared = generate_fit_data(
                        x_data, results,
                        fit_type="polynomial",
                        degree=FIT_DEGREE,
                        y_errors=plot_y_errors,
                        style=FIT_STYLE,
                        label=f'Polynomial Fit (degree {FIT_DEGREE})'
                    )
            else:
                coeffs, coeff_errors, r_squared = generate_fit_data(
                    x_data, results,
                    fit_type="polynomial",
                    degree=FIT_DEGREE,
                    y_errors=plot_y_errors,
                    style=FIT_STYLE,
                    label=FIT_LABEL
                )
            
            # Save fit results
            save_fit_results(
                output_filepath,
                coeffs,
                coeff_errors,
                r_squared,
                SIGNIFICANT_DIGITS,
                RESULT_UNIT
            )
        
        # Set plot properties
        plot_title = PLOT_TITLE if PLOT_TITLE else f'Results for {EXPERIMENT_NAME}'
        plot_xlabel = PLOT_XLABEL if PLOT_XLABEL else 'X'
        plot_ylabel = PLOT_YLABEL if PLOT_YLABEL else RESULT_NAME
        
        plt.title(plot_title)
        plt.xlabel(plot_xlabel)
        plt.ylabel(plot_ylabel)
        plt.grid(True)
        plt.legend()
        
        # Set axis limits if provided
        if PLOT_X_MIN is not None and PLOT_X_MAX is not None:
            plt.xlim(PLOT_X_MIN, PLOT_X_MAX)
        if PLOT_Y_MIN is not None and PLOT_Y_MAX is not None:
            plt.ylim(PLOT_Y_MIN, PLOT_Y_MAX)
        
        # Save plot
        plot_filepath = os.path.join(results_dir, f"plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(plot_filepath)
        print(f"Plot saved to: {plot_filepath}")
    
    # Save measurement results
    save_results(
        output_filepath,
        measurement_numbers,
        results,
        calc_errors,
        variables_dict,
        RESULT_NAME,
        RESULT_UNIT,
        SIGNIFICANT_DIGITS
    )
    print(f"\nAnalysis completed. \nResults saved to: {output_filepath}")

if __name__ == "__main__":
    main()
