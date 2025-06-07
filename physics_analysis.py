#!/usr/bin/env python3
"""
Physics Lab Data Analysis Script

Usage:
    1. Create a directory (e.g., labor_2/PS1) 
    2. Place your CSV data file and config file in that directory
    3. Run this script with: python physics_analysis.py path/to/config_file.py
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import importlib.util
import pandas as pd

# Add parent directory to sys.path to import package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import lab tools package
from physics_lab_tools import (
    write_to_file, 
    calculate_weighted_mean,
    calculate_results_with_errors,
    plot_data_with_errors,
    generate_fit_data,
    save_results,
    save_fit_results
)

def create_results_directory(base_dir):
    """Create a results directory if it doesn't exist."""
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    return results_dir

def load_config(config_path):
    """Dynamically load configuration from a Python file."""
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config

def read_csv_data(file_path):
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

def main():
    """Main analysis function"""
    
    # Check if config file path is provided
    if len(sys.argv) < 2:
        print("Usage: python physics_analysis.py path/to/config_file.py")
        sys.exit(1)
    
    # Load configuration from provided file
    config_path = sys.argv[1]
    config = load_config(config_path)
    
    print(f"Starting analysis for: {config.EXPERIMENT_NAME}")
    
    # Create results directory in the same folder as the config file
    base_dir = os.path.dirname(os.path.abspath(config_path))
    results_dir = create_results_directory(base_dir)
    output_filename = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    output_filepath = os.path.join(results_dir, output_filename)
    
    # Initialize output file
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(f"Analysis Results for {config.EXPERIMENT_NAME}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    # Prepare data arrays
    if config.USE_DIRECT_DATA:
        # Use data defined in config
        measurement_numbers = list(range(1, len(config.x_data) + 1))
        
        # Create measurements and errors arrays to match function expectations
        measurements = []
        errors = []
        
        # Extract data from config
        if hasattr(config, 'VARIABLES') and 'x' in config.VARIABLES and 'y' in config.VARIABLES:
            for i in range(len(config.x_data)):
                # Order matters! Ensure this matches the order in config.VARIABLES
                measurements.append([config.y_data[i], config.x_data[i]])
                errors.append([config.y_errors[i], config.x_errors[i]])
        
        # Variables dictionary for output
        variables_dict = {
            'X values': config.x_data,
            'Y values': config.y_data,
            'X errors': config.x_errors,
            'Y errors': config.y_errors
        }
    else:
        # Read data from CSV file
        csv_path = os.path.join(base_dir, config.DATA_FILE)
        df = read_csv_data(csv_path)
        
        # Get column names from config or try to infer from mapping
        x_col = config.X_COLUMN if hasattr(config, 'X_COLUMN') else 'X'
        y_col = config.Y_COLUMN if hasattr(config, 'Y_COLUMN') else 'Y'
        x_err_col = config.X_ERROR_COLUMN if hasattr(config, 'X_ERROR_COLUMN') else 'X_Error'
        y_err_col = config.Y_ERROR_COLUMN if hasattr(config, 'Y_ERROR_COLUMN') else 'Y_Error'
        
        # Try alternative column names if the preferred ones aren't found
        if x_col not in df.columns:
            possible_x = [col for col in df.columns if 'time' in col.lower() or 'x' in col.lower()]
            x_col = possible_x[0] if possible_x else df.columns[0]
            print(f"Using '{x_col}' as X column")
        
        if y_col not in df.columns:
            possible_y = [col for col in df.columns if 'temp' in col.lower() or 'y' in col.lower() or 'value' in col.lower()]
            y_col = possible_y[0] if possible_y else df.columns[1]
            print(f"Using '{y_col}' as Y column")
            
        if x_err_col not in df.columns:
            possible_x_err = [col for col in df.columns if 'error' in col.lower() and ('time' in col.lower() or 'x' in col.lower())]
            x_err_col = possible_x_err[0] if possible_x_err else None
            print(f"Using '{x_err_col}' as X error column" if x_err_col else "No X error column found")
            
        if y_err_col not in df.columns:
            possible_y_err = [col for col in df.columns if 'error' in col.lower() and ('temp' in col.lower() or 'y' in col.lower() or 'value' in col.lower())]
            y_err_col = possible_y_err[0] if possible_y_err else None
            print(f"Using '{y_err_col}' as Y error column" if y_err_col else "No Y error column found")
        
        # Extract data
        x_data = df[x_col].values
        y_data = df[y_col].values
        x_errors = df[x_err_col].values if x_err_col in df.columns else np.zeros_like(x_data)
        y_errors = df[y_err_col].values if y_err_col in df.columns else np.zeros_like(y_data)
        
        # Create measurement numbers
        measurement_numbers = list(range(1, len(x_data) + 1))
        
        # Create measurements and errors arrays
        measurements = []
        errors = []
        for i in range(len(x_data)):
            measurements.append([y_data[i], x_data[i]])
            errors.append([y_errors[i], x_errors[i]])
        
        # Variables dictionary for output
        variables_dict = {
            'X values': x_data,
            'Y values': y_data,
            'X errors': x_errors,
            'Y errors': y_errors
        }
    
    # Calculate results and errors
    num_measurements = len(measurements)
    results, calc_errors = calculate_results_with_errors(
        num_measurements,
        config.SCALING_FACTOR,
        config.FORMULA,
        config.VARIABLES,
        measurements,
        errors
    )
    
    # Calculate weighted mean if enabled
    if config.CALCULATE_WEIGHTED_MEAN:
        weighted_mean, weighted_mean_error = calculate_weighted_mean(results, calc_errors)
        write_to_file(
            output_filepath,
            f"Weighted Mean: {weighted_mean:.{config.SIGNIFICANT_DIGITS}g} {config.RESULT_UNIT}\n" +
            f"Weighted Mean Error: {weighted_mean_error:.{config.SIGNIFICANT_DIGITS}g} {config.RESULT_UNIT}\n"
        )
    
    # Create plot if enabled
    if config.PLOT_ENABLED:
        plt.figure(figsize=(10, 6))
        
        # Determine x and y data for plotting
        if config.USE_DIRECT_DATA:
            plot_x_data = config.x_data
        else:
            plot_x_data = x_data
            
        plot_y_data = results
        plot_y_errors = calc_errors if config.PLOT_SHOW_ERRORS else None
        
        # Plot data points
        plot_data_with_errors(
            plot_x_data, plot_y_data, plot_y_errors, None,
            style=config.PLOT_STYLE,
            label=config.PLOT_LABEL
        )
        
        # Add fit if enabled
        if config.FIT_ENABLED:
            if config.FIT_TYPE == "custom":
                fit_func = config.FIT_FUNCTION
                initial_guess = config.FIT_INITIAL_GUESS
                coeffs, coeff_errors, r_squared = generate_fit_data(
                    plot_x_data, plot_y_data,
                    fit_type="custom",
                    y_errors=plot_y_errors,
                    custom_fit_func=fit_func,
                    initial_guess=initial_guess,
                    style=config.FIT_STYLE,
                    label=config.FIT_LABEL
                )
            else:
                coeffs, coeff_errors, r_squared = generate_fit_data(
                    plot_x_data, plot_y_data,
                    fit_type="polynomial",
                    degree=config.FIT_DEGREE,
                    y_errors=plot_y_errors,
                    style=config.FIT_STYLE,
                    label=config.FIT_LABEL
                )
            
            # Save fit results
            save_fit_results(
                output_filepath,
                coeffs,
                coeff_errors,
                r_squared,
                config.SIGNIFICANT_DIGITS,
                config.RESULT_UNIT
            )
        
        # Set plot properties
        plt.title(config.PLOT_TITLE)
        plt.xlabel(config.PLOT_XLABEL)
        plt.ylabel(config.PLOT_YLABEL)
        plt.grid(True)
        plt.legend()
        
        # Set axis limits if provided
        if hasattr(config, 'PLOT_X_MIN') and hasattr(config, 'PLOT_X_MAX') and \
           config.PLOT_X_MIN is not None and config.PLOT_X_MAX is not None:
            plt.xlim(config.PLOT_X_MIN, config.PLOT_X_MAX)
        if hasattr(config, 'PLOT_Y_MIN') and hasattr(config, 'PLOT_Y_MAX') and \
           config.PLOT_Y_MIN is not None and config.PLOT_Y_MAX is not None:
            plt.ylim(config.PLOT_Y_MIN, config.PLOT_Y_MAX)
        
        # Save plot
        plot_filepath = os.path.join(results_dir, f"plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(plot_filepath)
        print(f"Plot saved to: {plot_filepath}")
        
        # Show plot
        plt.show()
    
    # Save measurement results
    save_results(
        output_filepath,
        measurement_numbers,
        results,
        calc_errors,
        variables_dict,
        config.RESULT_NAME,
        config.RESULT_UNIT,
        config.SIGNIFICANT_DIGITS
    )
    
    print(f"Analysis completed. Results saved to: {output_filepath}")

if __name__ == "__main__":
    main()
