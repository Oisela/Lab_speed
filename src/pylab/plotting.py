import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def plot_data_with_errors(x_data, y_data, y_errors=None, x_errors=None, 
                         style='bo', label='Measurements', capsize=5):
    """
    Plot data points with optional error bars.
    
    Args:
        x_data (np.ndarray): X-axis data
        y_data (np.ndarray): Y-axis data
        y_errors (np.ndarray, optional): Y-axis errors
        x_errors (np.ndarray, optional): X-axis errors
        style (str): Plot style
        label (str): Label for the legend
        capsize (int): Size of error bar caps
    """
    if y_errors is not None or x_errors is not None:
        plt.errorbar(x_data, y_data, yerr=y_errors, xerr=x_errors, 
                    fmt=style, label=label, capsize=capsize)
    else:
        plt.plot(x_data, y_data, style, label=label)

def generate_fit_data(x_data, y_data, fit_type='linear', degree=1, 
                     start_idx=None, end_idx=None, y_errors=None, 
                     custom_fit_func=None, initial_guess=None, style='r-', 
                     label=None):
    """
    Generate fit curve data and compute fit coefficients.
    
    Args:
        x_data (np.ndarray): X-axis data
        y_data (np.ndarray): Y-axis data
        fit_type (str): 'linear', 'polynomial', or 'custom'
        degree (int): Degree of polynomial fit
        start_idx (int, optional): Start index for fit range
        end_idx (int, optional): End index for fit range
        y_errors (np.ndarray, optional): Y-axis errors
        custom_fit_func (function, optional): Custom fit function
        initial_guess (list, optional): Initial guess for curve_fit
        style (str): Plot style
        label (str, optional): Label for the legend
        
    Returns:
        tuple: fit coefficients, coefficient errors, R²
    """
    # Extract data range for fitting
    if start_idx is not None and end_idx is not None:
        fit_x = x_data[start_idx:end_idx]
        fit_y = y_data[start_idx:end_idx]
        if y_errors is not None:
            fit_y_errors = y_errors[start_idx:end_idx]
        else:
            fit_y_errors = None
    else:
        fit_x = x_data
        fit_y = y_data
        fit_y_errors = y_errors
    
    # Perform fit based on type
    if fit_type == 'custom' and custom_fit_func is not None:
        if initial_guess is not None:
            coefficients, cov_matrix = curve_fit(
                custom_fit_func, fit_x, fit_y, p0=initial_guess, sigma=fit_y_errors
            )
        else:
            coefficients, cov_matrix = curve_fit(
                custom_fit_func, fit_x, fit_y, sigma=fit_y_errors
            )
        x_fit = np.linspace(min(fit_x), max(fit_x), 1000)
        y_fit = custom_fit_func(x_fit, *coefficients)
        residuals = fit_y - custom_fit_func(fit_x, *coefficients)
        
        if label is None:
            label = 'Custom Fit'
        
    else:  # polynomial fit (including linear)
        coefficients, cov_matrix = np.polyfit(fit_x, fit_y, degree, cov=True)
        x_fit = np.linspace(min(fit_x), max(fit_x), 1000)
        y_fit = np.polyval(coefficients, x_fit)
        residuals = fit_y - np.polyval(coefficients, fit_x)
        
        if label is None:
            if degree == 1:
                label = 'Linear Fit'
            else:
                label = f'Polynomial Fit (degree {degree})'
    
    # Calculate R²
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((fit_y - np.mean(fit_y))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # Coefficient errors
    coeff_errors = np.sqrt(np.diag(cov_matrix))
    
    # Plot the fit curve
    plt.plot(x_fit, y_fit, style, label=label)
    
    return coefficients, coeff_errors, r_squared
