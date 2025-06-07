"""
Configuration template for physics lab data analysis

This file serves as a template for configuring data analysis.
Copy this file to your experiment directory and modify it according to your needs.

If you dont want you to use some thing use "" or None
"""

import numpy as np
import sympy as sp

# Experiment information
EXPERIMENT_NAME = "Sample Physics Experiment"

# Data source configuration
USE_DIRECT_DATA = False  # Set to False to read from CSV file this will read the first file
DATA_FILE =  "ps2_data.csv"   # Name of CSV file in the same directory
DATA_FILE2 = ""  # Name of second CSV file in the same directory if "" not used
DATA_FILE3 = ""  # Name of second CSV file in the same directory if "" not used

# CSV column mapping (will be auto-detected if not specified)
AUTO_DETECT_COLUMNS = True  # Enable/disable automatic column detection
X_COLUMN = "Temperature"            # Column name for independent variable (e.g., Time)
Y_COLUMN = "Time"            # Column name for dependent variable (e.g., Temperature)
X_ERROR_COLUMN = "Time_Error" # Column name for independent variable error
Y_ERROR_COLUMN = "Temperature_Error" # Column name for dependent variable error

# Direct data input (only used if USE_DIRECT_DATA = True)
x_data = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]  # Independent variable values
y_data = [100.0, 82.0, 67.0, 55.0, 45.0, 37.0, 30.0, 25.0, 20.0, 16.0]  # Dependent variable values
x_errors = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]  # Independent variable errors
y_errors = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]  # Dependent variable errors

# Analysis configuration
FORMULA = "x * 10 "  # Formula to calculate results
VARIABLES = "y x"  # Variables in the formula (space-separated, must match order used in calculations)
SCALING_FACTOR = 1.0  # Scaling factor for results
SIGNIFICANT_DIGITS = 3  # Number of significant digits for results
CALCULATE_WEIGHTED_MEAN = True  # Calculate weighted mean of results

# Result information
RESULT_NAME = "Time Constant"  # Name of the calculated result
RESULT_UNIT = "s"  # Unit of the calculated result

# Plotting configuration
PLOT_ENABLED = True  # Enable/disable plotting
PLOT_TITLE = "Physics Lab Measurement Results"  # Plot title
PLOT_XLABEL = "Time (s)"  # X-axis label
PLOT_YLABEL = "Temperature (°C)"  # Y-axis label
PLOT_STYLE = "ro"  # Plot style for data points
PLOT_LABEL = "Measured Data"  # Label for data points
PLOT_SHOW_ERRORS = True  # Show error bars
PLOT_X_MIN = None  # Minimum value for x-axis (None for auto)
PLOT_X_MAX = None  # Maximum value for x-axis (None for auto)
PLOT_Y_MIN = None  # Minimum value for y-axis (None for auto)
PLOT_Y_MAX = None  # Maximum value for y-axis (None for auto)

# Fitting configuration
FIT_ENABLED = True  # Enable/disable fitting
FIT_TYPE = "polynomial"  # "polynomial" or "custom"
FIT_DEGREE = 1  # Degree of polynomial fit (if FIT_TYPE is "polynomial")
FIT_FUNCTION = lambda x, a, b: a * x + b  # Custom fit function (if FIT_TYPE is "custom")
FIT_INITIAL_GUESS = [1, 0]  # Initial guess for parameters (if FIT_TYPE is "custom")
FIT_STYLE = "b-"  # Plot style for fit line
FIT_LABEL = "Fit Curve"  # Label for fit line
