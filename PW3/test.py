import numpy as np
import matplotlib.pyplot as plt

# Daten
plot_xdata = np.array([500, 510, 520, 530, 540])  # Wellenlängen in nm
plot_ydata = np.array([1.60806, 1.61168, 1.61461, 1.63228, 1.64163])  # Messwerte

# Grad des Polynoms
fit_grad = 2

# Polynom anpassen
coefficients = np.polyfit(plot_xdata, plot_ydata, fit_grad)
print("Fit-Koeffizienten:", coefficients)

# Feiner x-Bereich für den Fit
x_fit = np.linspace(min(plot_xdata), max(plot_xdata), 1000)
fit_y = np.polyval(coefficients, x_fit)

# Plotten
plt.plot(plot_xdata, plot_ydata, 'bo', label='Datenpunkte')
plt.plot(x_fit, fit_y, 'r--', label='Polynomfit 2. Ordnung')
plt.xlabel('Wellenlänge (nm)')
plt.ylabel('Brechungsindex')
plt.legend()
plt.show()
