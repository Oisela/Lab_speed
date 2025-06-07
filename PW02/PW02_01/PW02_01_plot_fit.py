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



# Gegeben: Massen m1, m2
m1 = 0.02 # 
m2 = 0.9983  # Beispielwert in kg, durch echte Werte ersetzen
g = 9.81  # Erdbeschleunigung in m/s^2


# Daten ein Lesen für VCS
filename = r"PW02\PW02_01\PW2_01_ST.txt"

t_list, x_list, y_List = [], [], []

read_data(filename, t_list, x_list, y_List)

x_array = np.array(x_list)
y_array = np.array(y_List)
t_array = np.array(t_list)



# Polynomfit 2. Ordnung (ax^2 + bx + c) durchführen
coefficients = np.polyfit(t_array, y_array, 2)

# Die Koeffizienten sind in absteigender Ordnung: [a, v0, x0]
a = coefficients[0]
v0 = coefficients[1]
y0 = coefficients[2]

# Angepasste Parabel basierend auf den Fit-Koeffizienten berechnen
fit_x = a * t_array**2 + v0 * t_array + y0

# Ergebnisse ausgeben
print(f"Ermittelter Wert für a: {a}")
print(f"Ermittelter Wert für v0: {v0}")
print(f"Ermittelter Wert für x0: {y0}")



# Berechnung der experimentellen Kraft
F_e = (m1 + m2) * a # Kraft aus der Bewegungsgleichung F = m * a
F_r = m1 * g        # 
F_N = m2 * g

# Berechnung des Gleitreibungskoeffizienten
mu_G = (F_r - F_e) / F_N

# Ergebnisse ausgeben
print(f"Kraft des Bewegten Systems: {F_e:.3f} N")
print(f"Normal Kraft: {F_N:.3f} N")
print(f"Reibungskraft: {F_r:.3f} N")

print(f"Gleitreibungskoeffizient µG: {mu_G:.3f}")

Datei_Erg = "PW02\PW02_01\ergebnisse.txt"
# Ergebnisse in eine Textdatei schreiben
with open(Datei_Erg, "w") as file:
    file.write(f"Ermittelter Wert für a: {a}\n")
    file.write(f"Ermittelter Wert für v0: {v0}\n")
    file.write(f"Ermittelter Wert für x0: {y0}\n")
    file.write(f"Experimentelle Kraft: {F_r:.3f} N\n")
    file.write(f"Theoretische Kraft (reibungsfrei): {F_N:.3f} N\n")
    file.write(f"Gleitreibungskoeffizient µG: {mu_G:.3f}\n")



# Originaldaten und die angepasste Funktion plotten
plt.figure(figsize=(10, 6))  # Vergrößert die Skala des Plots
plt.plot(t_array, y_array, 'bo', label='Messdaten')  # Blaue Punkte für die Messdaten
plt.plot(t_array, fit_x, 'r-', label='Polynomfit 2. Ordnung')  # Rote Linie für den Polynomfit
plt.xlabel('Zeit (s)')
plt.ylabel('Position y(t) (m)')
plt.title('Gleichmässig beschleunigte Bewegung')
plt.legend()
plt.grid(True)

# Diagramm anzeigen
plt.show()