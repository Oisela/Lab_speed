import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
# ---------------------------
# Schritt 0: Beispiel-Daten
# ---------------------------
freq_kHz = np.array([
    3.9, 4.2, 4.4, 4.6, 4.7, 4.8, 4.85, 4.91, 4.92, 4.93,
    4.94, 4.95, 4.96, 4.97, 4.98, 4.99, 5.0, 5.02, 5.05,
    5.08, 5.11, 5.15, 5.2, 5.25, 5.4, 5.6, 7.1, 8.0
])
amp_mV = np.array([
    32, 48, 80, 112, 144, 240, 336, 624, 736, 800,
    896, 928, 936, 912, 824, 768, 720, 576, 416,
    336, 304, 224, 200, 160, 128, 96, 48, 32
])

# In rad/s umwandeln (optional)
omega = 2 * np.pi * 1000 * freq_kHz

# ---------------------------
# Schritt 1: Lorentz-Funktion
# ---------------------------
def lorentzian(x, A, x0, gamma, offset):
    """Lorentz-Funktion für resonanzartige Peaks."""
    return A * gamma**2 / ((x - x0)**2 + gamma**2) + offset



# ---------------------------
# Schritt 2: Fit ausführen
# ---------------------------
# Schätzwerte für Parameter: [Amplitude, Resonanzstelle, Breite, Offset]
initial_guess = [900, 3.1e4, 1.5e3, 0]

# curve_fit an Lorentz-Funktion
popt, pcov = curve_fit(lorentzian, omega, amp_mV, p0=initial_guess)
A_fit, x0_fit, gamma_fit, offset_fit = popt

# ---------------------------
# Schritt 3: R^2 berechnen
# ---------------------------
# Vorhersage des Fits für die Original-x-Werte
amp_fit = lorentzian(omega, *popt)  

# Residuen
residuals = amp_mV - amp_fit
# Quadratische Abweichungen
ss_res = np.sum(residuals**2)
# Gesamtvarianz relativ zum Mittelwert
ss_tot = np.sum((amp_mV - np.mean(amp_mV))**2)
# Bestimmtheitsmaß R^2
r_squared = 1 - (ss_res / ss_tot)

# ---------------------------
# Schritt 4: Plot erstellen
# ---------------------------
plt.figure(figsize=(8, 5))

# Messdaten in Blau
plt.scatter(omega, amp_mV, label="Messdaten", color="blue", s=30)

# Für den Plot einen glatten Bereich generieren
omega_fit = np.linspace(min(omega), max(omega), 400)
amp_smooth = lorentzian(omega_fit, *popt)

# Fit in Grün
plt.plot(omega_fit, amp_smooth, color="green", label="Lorentz-Fit")

plt.xlabel(r'Kreisfrequenz $\omega$ (rad/s)')
plt.ylabel('Amplitude (mV)')
#plt.title('Resonanzkurve mit Lorentz-Fit')

# Im Plot R^2 in die rechte obere Ecke schreiben
plt.text(
    0.98, 0.95,
    f"R² = {r_squared:.4f}",
    ha='right', va='top',
    transform=plt.gca().transAxes,  # Koordinaten relativ zum Achsenbereich
    bbox=dict(facecolor='white', alpha=0.7, boxstyle='round')
)
plot = True
Dateiname_Ergebnisse = "Er_" + os.path.basename(__file__).replace('.py', '') + ".txt"
ordner = os.path.join(os.path.dirname(__file__), "Ergebnisse")
if not os.path.exists(ordner):
    os.makedirs(ordner)
# Pfad zur Datei im "Ergebnisse" Ordner
dateipfad = os.path.join(ordner, Dateiname_Ergebnisse)
plt.legend()
plt.grid(True)
# Plot anzeigen
if plot:
    #plt.show()
    plotname = dateipfad.replace('.txt', '.png')
    plotname = plotname.replace('Er_', 'Plot_')
    plt.savefig(plotname)
    print(f"Der Plot wurde als '{plotname}' gespeichert.")

# ---------------------------
# Ergebnisse ausgeben
# ---------------------------
print("=== Gefundene Parameter (Lorentz) ===")
print(f"A      = {A_fit:.3f} mV")
print(f"x0     = {x0_fit:.1f} rad/s")
print(f"gamma  = {gamma_fit:.1f} rad/s")
print(f"offset = {offset_fit:.3f} mV")
print(f"R^2    = {r_squared:.5f}")
