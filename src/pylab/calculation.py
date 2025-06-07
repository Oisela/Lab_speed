import numpy as np
import sympy as sp
from scipy.optimize import curve_fit

def error_propagation(formula_str, variables_str, measurements, errors):
    """
    Calculate error propagation using the Gaussian method with absolute errors.
    
    Args:
        formula_str (str): Mathematical formula as string
        variables_str (str): Variables in the formula as space-separated string
        measurements (list): List of measurement values for variables
        errors (list): List of absolute errors for variables
        
    Returns:
        tuple: Calculated value and total error
    """
    # Create symbols
    variables = sp.symbols(variables_str)
    formula = sp.sympify(formula_str)
    
    # Calculate partial derivatives
    derivatives = [formula.diff(var) for var in variables]
    
    # Substitute values
    values_dict = dict(zip(variables, measurements))
    formula_value = float(formula.evalf(subs=values_dict))
    
    # Calculate error propagation
    squared_error = 0
    for dfdx, delta in zip(derivatives, errors):
        dfdx_value = float(dfdx.evalf(subs=values_dict))
        squared_error += (dfdx_value * delta)**2
    
    total_error = np.sqrt(squared_error)
    
    return formula_value, total_error

def calculate_weighted_mean(values, errors):
    """
    Calculate weighted mean and its error based on individual measurement errors.
    
    Args:
        values (list or np.ndarray): List of values
        errors (list or np.ndarray): List of errors
        
    Returns:
        tuple: Weighted mean and its error
    """
    weights = 1 / np.array(errors)**2
    weighted_sum = np.sum(weights * values)
    sum_of_weights = np.sum(weights)
    weighted_mean = weighted_sum / sum_of_weights
    weighted_mean_error = 1 / np.sqrt(sum_of_weights)
    
    return weighted_mean, weighted_mean_error

def calculate_results_with_errors(num_measurements, scaling_factor, formula, variables, measurements, errors):
    """
    Calculate results and errors for multiple measurements.
    
    Args:
        num_measurements (int): Number of measurements
        scaling_factor (float): Scaling factor for results
        formula (str): Formula as string
        variables (str): Variables as space-separated string
        measurements (list): List of measurements
        errors (list): List of errors
        
    Returns:
        tuple: Lists of calculated results and errors
    """
    results = []
    calc_errors = []
    
    for i in range(num_measurements):
        # Calculate result and error
        result, error = error_propagation(formula, variables, measurements[i], errors[i])
        
        # Scale result
        scaled_result = result * scaling_factor
        scaled_error = error * scaling_factor
        
        # Add to lists
        results.append(scaled_result)
        calc_errors.append(scaled_error)
        
    return results, calc_errors


