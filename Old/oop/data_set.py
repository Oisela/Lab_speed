import numpy as np


class data_set:
    def __init__(self, variable_name, values, errors, unit, file_path):
        self.var_name = variable_name
        self.values =  values
        self.errors = errors
        self.unit = unit
        self.file_path = file_path
        # Ensure inputs are lists
        with open(file_path, 'a', encoding='utf-8') as f:
                # Write variables and their values
                f.write("\n")
                f.write("LaTeX equation format:\n\n")
                f.write("\\begin{align*}\n")
                f.write(f"\t{self.var_name} &= \\SI{{{self.values}({self.errors})}}{{\\{self.unit}}}\n")
                f.write("\\end{align*}\n\n")


    
    def calculate_mean(self):
        return np.mean(self.val)
    
