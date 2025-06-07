import os
from .utils import write_to_file, format_scientific_error

def save_results(file_path, measurement_nums, results, errors, variables_dict, 
               result_name, result_unit, significant_digits=2):
    """
    Save calculation results to a file.
    
    Args:
        file_path (str): Path to the output file
        measurement_nums (list): List of measurement numbers
        results (list): List of calculated results
        errors (list): List of calculated errors
        variables_dict (dict): Dictionary of variables and their values
        result_name (str): Name of the result
        result_unit (str): Unit of the result
        significant_digits (int): Number of significant digits
    """
    with open(file_path, 'a', encoding='utf-8') as f:
        # Write variables and their values
        f.write("Variables and values used:\n")
        for var_name, var_value in variables_dict.items():
            f.write(f"{var_name} = {var_value}\n")
        f.write("\n")
        
        # Write header
        f.write(f"{'Measurement':<10}{f'{result_name} ({result_unit})':<20}{f'Error ({result_unit})':<20}\n")
        
        # Write results
        for i, result, error in zip(measurement_nums, results, errors):
            f.write(f"{i:<10.{significant_digits}g}{result:<20.{significant_digits}g}{error:<20.{significant_digits}g}\n")
        
        # LaTeX table for results
        if len(results) > 1:
            f.write("\n")
            f.write("LaTeX table format:\n\n")
            f.write("\\begin{table}[H]\n")
            f.write("\t\\centering\n")
            f.write("\t\\begin{tabular}{|c|c|}\n")
            f.write(f"\t\t\\hline Measurements & {result_name} (${result_unit}$) \\\\\\hline\n")
            
            for i, result, error in zip(measurement_nums, results, errors):
                formatted_error = errors
                if float(formatted_error) >= 10 or float(formatted_error) <= 1:
                    error_length = 0
                else:
                    error_length = len(str(formatted_error).split(".")[1])
                
                f.write(f"\t\t\\hline {i} & ${result:.{error_length}f} \\pm {formatted_error}$ \\\\\n")
            
            f.write("\t\t\\hline\n")
            f.write("\t\\end{tabular}\n")
            f.write(f"\t\\caption{{Measurement results for {result_name}}}\n")
            f.write(f"\t\\label{{tab:{result_name.replace(' ', '_')}}}\n")
            f.write("\\end{table}\n\n")
        
        # For single measurements, write in equation format
        if len(results) == 1:
            f.write("\n")
            f.write("LaTeX equation format:\n\n")
            f.write("\\begin{align*}\n")
            f.write(f"\t{result_name} &= \\SI{{{results[0]:.{significant_digits}g}({errors[0]:.{significant_digits}g})}}{{\\{result_unit}}}\n")
            f.write("\\end{align*}\n\n")

def save_fit_results(file_path, coefficients, coeff_errors, r_squared, 
                   significant_digits=2, result_unit=""):
    """
    Save fit results to a file.
    
    Args:
        file_path (str): Path to the output file
        coefficients (np.ndarray): Fit coefficients
        coeff_errors (np.ndarray): Errors of fit coefficients
        r_squared (float): R-squared value
        significant_digits (int): Number of significant digits
        result_unit (str): Unit for results
    """
    text = "Fit Results:\n\n"
    
    # Coefficients and their errors
    for i, (coeff, error) in enumerate(zip(coefficients, coeff_errors)):
        text += f"Coef. {i}: {coeff:.{significant_digits}g} ± {error:.{significant_digits}g}\n"
    
    
    text += f"R² = {r_squared:.5f}\n\n"
    
    # LaTeX format
    text += "LaTeX format:\n"
    text += "\\begin{align*}\n"
    text += f"\tR^2 &= {r_squared:.5f}\n"
    
    for i, (coeff, error) in enumerate(zip(coefficients, coeff_errors)):
        text += f"\ta_{i} &= \\SI\n"
    
    text += "\\end{align*}\n\n"
    
    write_to_file(file_path, text)

def save_result(file_path, result_name, result, error, einheit):
    # Ensure inputs are lists
    if not isinstance(result_name, list):
        result_name = [result_name]
    if not isinstance(result, list):
        result = [result]
    if not isinstance(error, list):
        error = [error]
    if not isinstance(einheit, list):
        einheit = [einheit]

    with open(file_path, 'a', encoding='utf-8') as f:
        # Write variables and their values
        f.write("\n")
        f.write("LaTeX equation format:\n\n")
        f.write("\\begin{align*}\n")
        for i in range(len(result)):
            f.write(f"\t{result_name[i]} &= \\SI{{{result[i]}({error[i]})}}{{\\{einheit[i]}}}\n")
        f.write("\\end{align*}\n\n")

def save_result_dict(file_path, dict):
    # Ensure inputs are lists

    with open(file_path, 'a', encoding='utf-8') as f:
        # Write variables and their values
        f.write("\n")
        f.write("LaTeX equation format:\n\n")
        f.write("\\begin{align*}\n")
        for i in range(len(dict["result_name"])):
            f.write(f"\t{dict["result_name"][i]} &= \\SI{{{dict["values"][i]}({dict["errors"][i]})}}{{\\{dict["einheit"][i]}}}\n")
        f.write("\\end{align*}\n\n")