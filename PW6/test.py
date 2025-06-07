import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

# Beispielhafte Daten (ersetze sie durch deine tatsächlichen Daten)
spannung = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])  # Spannung in V
strom = np.array([1.4e-5, 1.3e-5, 1.2e-5, 1.1e-5, 9.0e-6, 8.0e-6])  # Strom in A

# Fit mit einem Polynom 2. Ordnung
poly_fit = Polynomial.fit(spannung, strom, 2)
poly_fit_coefs = poly_fit.convert().coef

# Berechne den angepassten Stromwert
spannung_fine = np.linspace(spannung.min(), spannung.max(), 100)
strom_fit = poly_fit(spannung_fine)

# Plotten der Messdaten und des angepassten Fits
plt.errorbar(spannung, strom, yerr=0.1e-5, fmt='o', label='Messwerte', color='blue', markersize=6)

# Plotten der Polynomfit-Linie
plt.plot(spannung_fine, strom_fit, 'r--', label='Polynomfit 2. Ordnung')

# Berechne den R^2-Wert für die Güte der Anpassung
residuals = strom - poly_fit(spannung)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((strom - np.mean(strom))**2)
r_squared = 1 - (ss_res / ss_tot)

# R²-Wert im Diagramm anzeigen
plt.text(1.5, 1.1e-5, f'$R^2 = {r_squared:.4f}$', fontsize=12)

plt.xlabel('Spannung (V)')
plt.ylabel('Strom (A)')
plt.title('Polynomfit 2. Ordnung der Kennlinie')
plt.legend()
plt.grid()
plt.show()

