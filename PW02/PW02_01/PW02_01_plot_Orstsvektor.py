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

x_array = np.array(x_list)
y_array = np.array(y_List)
t_array = np.array(t_list)



# Betrag des Ortsvektors berechnen
r_array = np.sqrt(x_array**2 + y_array**2)

# Bewegungsdiagramm x(t) erstellen
plt.figure()
plt.plot(t_array, r_array, marker='o', linestyle='-', label='Ortsvektorbetrag r(t)')

# Achsenbeschriftungen und Titel
plt.xlabel('Zeit (s)')
plt.ylabel('Betrag des Ortsvektors r(t) (m)')
plt.title('Bewegungsdiagramm: Ortsvektorbetrag als Funktion der Zeit')
plt.legend()
plt.grid(True)

# Diagramm anzeigen
plt.show()