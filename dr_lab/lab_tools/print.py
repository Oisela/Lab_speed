import numpy as np
from scipy import stats

significant_digits = 4

def latex_results(result_name, result_unit, results, errors, file_path):
     with open(file_path, 'a', encoding='utf-8') as f:
        f.write("\n")
        f.write("LaTeX equation format:\n\n")
        f.write("\\begin{align*}\n")
        f.write(f"\t{result_name} &= \\SI{{{results:.{significant_digits}g}({errors:.{significant_digits}g})}}{{\\{result_unit}}}\n")
        f.write("\\end{align*}\n\n")