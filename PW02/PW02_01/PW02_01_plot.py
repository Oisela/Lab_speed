import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import os  # Für Dateioperationen
import sympy as sp
import datetime  # Für Datum und Zeit
# Add the path to the directory containing the module
sys.path.append(os.path.abspath('../Master_Labor'))
from Maindef import *


# Daten ein Lesen für VCS
filename = r"PW02\PW02_01\PW2_01_ST.txt"

t_list, x_list, y_List = [], [], []

read_data(filename, t_list, x_list, y_List)

# Convert lists to numpy arrays for easier manipulation
t_array = np.array(t_list)
x_array = np.array(x_list)
y_array = np.array(y_List)
# Create a new figure
plt.figure()

# Plot s-t diagram
plt.plot(t_array, y_array, label='Masse 01')

# Add labels and title
plt.xlabel('Zeit (s)')
plt.ylabel('Y-Position (m)')
plt.title('Gleichmäßig beschleunigte Bewegung')
plt.legend()
plt.grid(True)
# Show the plot
plt.show()


