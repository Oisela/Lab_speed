## Version: 1.0$
## Date: 2021-09-29$
## Author: A. Ospelt

# Dieses Programm kann folgende Aufgaben erledigen:
# - Berechnung der Fehlerfortpflanzung für eine gegebene Formel
# - Berechnung des Mittelwerts und der Standardabweichung der Ergebnisse
# - Erstellung eines Plots der Messwerte mit optionaler Fit-Kurve
# - Speichern der Ergebnisse in einer Textdatei

# Die Eingaben erfolgen im Abschnitt "Eingabe" und die Ausgaben werden in den Dateien im Ordner "Ergebnisse" gespeichert.




import numpy as np
import os  # Für Dateioperationen
import sympy as sp
import subprocess
import sys
import matplotlib.pyplot as plt
# -------------------------------
# Variablendefinitionen
# -------------------------------


anzahl_messungen = 6  # Kann leicht angepasst werden
skalierung = 1  # Skalierungsfaktor für die Ergebnisse (z.B. 1000 für mPa·s)
ergebnis_einheit = 'Rad'  # Einheit des Ergebnisses
ergebnis_name = 'Ablenkungswinkel'  # Name des Ergebnisses
Signifikante_Stellen = 5    # Anzahl der signifikanten Stellen
# Hier kannst du alle Variablen und Konstanten definieren, die du benötigst
d, L = sp.symbols('d L')

# Formel mit SymPy-Funktionen definieren
formel = sp.atan(d * (L*2)**-1)

# Definiere die Variablen als String (Reihenfolge muss mit den Daten übereinstimmen)
variablen = 'd L'

# Konstanten (für alle Messungen gleich)
L = 1.256 # Länge in Meter

# Absolute Fehler der Konstanten
fehler_L = 0.003  # Fehler bei 'L' in Meter


# Messwerte 
d = np.array([
    0.017, 
    0.034, 
    0.049, 
    0.067,
    0.084, 
    0.1
    ])  # Winkel in Grad

# Fehler Messerte
fehler_d = [0.0015] * anzahl_messungen  # Absoluter Fehler von 0.4 Sekunden

# Variablen und deren Werte sammeln
variablen_werte = {
    'Länge von Spalt zu Blatt': L,
    'Fehler L': fehler_L,
    'Breite Beugung': d,
    'Fehler d': fehler_d
    
}

# Werte für jede Variable
# Verwende [i] für die Indizierung, um die Werte für jede Messung zu speichern

Laser = 650 * 10**-9

LaserN = [Laser * (i + 1) for i in range(anzahl_messungen)]


## Reihenfolge beachten ##
messwerte = [
    [d[i], L] for i in range(anzahl_messungen) 
]
# Fehler für jede Variable
fehler = [
    [fehler_d[i], fehler_L] for i in range(anzahl_messungen)
]
messungsnummern = list(range(1, anzahl_messungen + 1))

# Plot Einstellungen
plot = True                                # Plot erstellen
plot_xlabel = r'Winekl $\alpha_{min}$ in Radiant'                 # Beschriftung der x-Achse
plot_ylabel = r'$n \lambda$ in $m$'  # Beschriftung der y-Achse
plot_titel  = '' # Titel des Plots
plot_error = False                # Fehlerbalken im Plot anzeigen
plot_xdata = LaserN  # x-Achse: wenn Messungezahal, dann : Messungsnummern
plot_fit = True                  # Fit-Kurve im Plot anzeigen
fit_grad = 1  # Hier den gewünschten Grad des Fits angeben

# Variablen für den Start- und Endpunkt der x- und y-Achse und die Option, dies zu aktivieren
Plot_Auto = False # Automatische Skalierung der Achsen

plot_x_start = None # Startpunkt der x-Achse (None bedeutet automatisch)
plot_x_end = None  # Endpunkt der x-Achse (None bedeutet automatisch)
plot_y_start = 0.000   # Startpunkt der y-Achse (None bedeutet automatisch)
plot_y_end = 0.000005 # Endpunkt der y-Achse (None bedeutet automatisch)




##################
## Eingabe Ende ##
##################

# Optionen für den Plot Auto
if plot == False:
    plot_error = False
    plot_fit = False

if Plot_Auto == True:
    plot_start_at_zero = False
    plot_x_start = None
    plot_x_end = None
    plot_y_start = None
    plot_y_end = None   

# Messungsnummern für die Ausgabe
messungsnummern = list(range(1, anzahl_messungen + 1))

#################### Berechnungen ####################

def fehlerfortpflanzung(formel_str, variablen_str, messwerte, fehler):
    """
    Berechnet die Fehlerfortpflanzung nach der Gauß'schen Methode mit absoluten Fehlern.

    Args:
        formel_str (str): Die mathematische Formel als String.
        variablen_str (str): Die Variablen in der Formel als String, getrennt durch Leerzeichen.
        messwerte (list): Liste der Messwerte für die Variablen.
        fehler (list): Liste der absoluten Fehler für die Variablen.

    Returns:
        tuple: Berechneter Wert und Gesamtfehler.
    """
    # Symbole erstellen
    variablen = sp.symbols(variablen_str)
    formel = sp.sympify(formel_str)
    
    # Partielle Ableitungen berechnen
    ableitungen = [formel.diff(var) for var in variablen]
    # Werte einsetzen
    werte_dict = dict(zip(variablen, messwerte))
    formel_wert = float(formel.evalf(subs=werte_dict))

    # Fehlerfortpflanzung berechnen
    quadratischer_fehler = 0
    for dfdx, delta in zip(ableitungen, fehler):
        dfdx_wert = float(dfdx.evalf(subs=werte_dict))
        quadratischer_fehler += (dfdx_wert * delta)**2
    gesamtfehler = np.sqrt(quadratischer_fehler)
    

    
    return formel_wert, gesamtfehler

def speichere_ergebnisse(dateiname, messungsnummern, ergebnisse, fehler, variablen_werte,
                         mittelwert_ergebnis, mittelwert_fehler,
                         standardabweichung=None, standardfehler=None, coefficients=None, coeff_errors=None):
    """
    Speichert die Ergebnisse in eine Textdatei, überschreibt bestehende Daten.
    Fügt die verwendeten Variablen und deren Werte hinzu sowie den Mittelwert und den mittleren Fehler.

    Args:
        dateiname (str): Name der Datei, in die die Ergebnisse gespeichert werden.
        messungsnummern (list of int): Liste der Messungsnummern.
        ergebnisse (list of float): Liste der berechneten Ergebnisse.
        fehler (list of float): Liste der berechneten Fehler.
        variablen_werte (dict of str: float): Dictionary mit Variablennamen und deren Werten.
        mittelwert_ergebnis (float): Mittelwert der Ergebnisse.
        mittelwert_fehler (float): Mittelwert der Fehler.
        standardabweichung (float, optional): Standardabweichung der Ergebnisse.
        standardfehler (float, optional): Standardfehler des Mittels.
        coefficients (list of float, optional): Liste der Koeffizienten des Fits.
        coeff_errors (list of float, optional): Liste der Fehler der Koeffizienten des Fits.
    """
    # Ordner "Ergebnisse" erstellen, falls er nicht existiert
    ordner = "Ergebnisse"
    if not os.path.exists(ordner):
        os.makedirs(ordner)

    # Pfad zur Datei im "Ergebnisse" Ordner
    dateipfad = os.path.join(ordner, dateiname)

    try:
        # Datei im Schreibmodus öffnen ('w' für write), um bestehende Daten zu überschreiben
        with open(dateipfad, 'w', encoding='utf-8') as f:
            # Variablen und deren Werte schreiben
            f.write("Verwendete Variablen und Werte:\n")
            for var_name, var_value in variablen_werte.items():
                f.write(f"{var_name} = {var_value}\n")
            f.write("\n")

            # Header schreiben
            f.write(f"{'Messung':<10}{f'{ergebnis_name} ({ergebnis_einheit})':<20}{f'Fehler ({ergebnis_einheit})':<20}\n")

            # Ergebnisse schreiben
            for i, n, dn in zip(messungsnummern, ergebnisse, fehler):
                f.write(f"{i:<10}{n:<20.{Signifikante_Stellen}g}{dn:<20.{Signifikante_Stellen}g}\n")

            # Mittelwerte schreiben
            f.write("\n")
            f.write(f"Mittelwert der {ergebnis_name}: {mittelwert_ergebnis:.{Signifikante_Stellen}g} {ergebnis_einheit}\n")
            f.write(f"Mittelwert der Fehler: {mittelwert_fehler:.{Signifikante_Stellen}g} {ergebnis_einheit}\n")

            # Optional: Standardabweichung und Standardfehler des Mittels schreiben
            if standardabweichung is not None:
                f.write(f"Standardabweichung: {standardabweichung:.{Signifikante_Stellen}g} {ergebnis_einheit}\n")
            if standardfehler is not None:
                f.write(f"Standardfehler des Mittels: {standardfehler:.{Signifikante_Stellen}g} {ergebnis_einheit}\n")
                f.write(f"Ergebniss: {mittelwert_ergebnis:.{Signifikante_Stellen}g} ± {standardfehler:.{Signifikante_Stellen}g} {ergebnis_einheit}\n")


            # Optional: Fit-Koeffizienten und deren Fehler schreiben
            if coefficients is not None:
                f.write("\nFit-Koeffizienten:\n")
                for i, (coeff, error) in enumerate(zip(coefficients, coeff_errors)):
                    f.write(f"Koef. {i}: {coeff:.{Signifikante_Stellen}g} ± {error:.{Signifikante_Stellen}g}\n")
            
            # LaTeX-Formatierung
            if len(ergebnisse) > 1:
                f.write("\n")
                # Ergebnisse schreiben (für LaTeX)
                f.write("Ergebnisse für LaTeX:\n")
                f.write("\n")
                f.write("\\begin{table}[H] \n")
                f.write("\t \\centering \n" )
                f.write("\t \\begin{tabular}{|c|c|} \n")
                f.write(f"\t \t \hline Messungen & {ergebnis_name} ({ergebnis_einheit})  \\\ \hline \n")
                for i, n, dn in zip(messungsnummern, ergebnisse, fehler):
                    f.write(f"\t \t \hline {i} & ${n:.{Signifikante_Stellen}g} \pm {dn:.{Signifikante_Stellen}g}$ \\\ \n")
                f.write("\t \t \\hline \n")
                f.write("\t \\end{tabular} \n")
                f.write(f"\t \caption{{Messergebnisse für {ergebnis_name} }} \n")
                f.write(f"\t \\label{{tab:{ergebnis_name}}} \n")
                f.write("\\end{table} \n")
                f.write("\n")
            
            # Bei nur einer Messung, schreibe die Ergebnisse in eine separate Zeile
            if len(ergebnisse) == 1:
                f.write("\n")
                # Ergebnisse schreiben (für LaTeX)
                f.write("Ergebnisse für LaTeX:\n")
                f.write("\n")
                f.write("\\begin{align*} \n")
                f.write(f"\t ? &= \\SI{{{ergebnisse[0]:.{Signifikante_Stellen}g}({fehler[0]:.{Signifikante_Stellen}g})}}{{\\{ergebnis_einheit}}} \n" )
                f.write("\\end{align*} \n")
                f.write("\n")





        print(f"Die Ergebnisse wurden in die Datei '{dateipfad}' geschrieben.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# -------------------------------
# Berechnungen durchführen
# -------------------------------

# Listen zur Speicherung der berechneten Ergebnisse und Fehler
berechnete_ergebnisse = []
berechnete_fehler = []

# Schleife über jede Messung
for i in range(anzahl_messungen):
    # Ergebnis und Fehler berechnen
    ergebnis, gesamtfehler = fehlerfortpflanzung(formel, variablen, messwerte[i], fehler[i])
    
    # Ergebnis skalieren
    ergebnis_skaliert = ergebnis * skalierung
    gesamtfehler_skaliert = gesamtfehler * skalierung
    
    # Zu Listen hinzufügen
    berechnete_ergebnisse.append(ergebnis_skaliert)
    berechnete_fehler.append(gesamtfehler_skaliert)

# -------------------------------
# Mittelwerte und Statistiken berechnen
# -------------------------------

# Mittelwert der Ergebnisse und Fehler berechnen
mittelwert_ergebnis = np.mean(berechnete_ergebnisse)
mittelwert_fehler = np.mean(berechnete_fehler)



# Standardabweichung und Standardfehler des Mittels berechnen (wenn mehr als eine Messung)
if anzahl_messungen > 1:
    standardabweichung = np.std(berechnete_ergebnisse, ddof=1)
    standardfehler_des_mittels = standardabweichung / np.sqrt(anzahl_messungen)
else:
    standardabweichung = None
    standardfehler_des_mittels = None



# Plot erstellen
plot_ydata = berechnete_ergebnisse


#changed
change_data = True
if change_data:
    temp_plot_xdata = plot_ydata
    temp_plot_ydata = plot_xdata
    plot_xdata = temp_plot_xdata
    plot_ydata = temp_plot_ydata


plt.figure(figsize=(10, 6))


if plot_error:
    plt.errorbar(plot_xdata, plot_ydata, yerr=berechnete_fehler, fmt='o', label='Messwerte', capsize=5)
else:
    plt.plot(plot_xdata, plot_ydata, 'o', label='Messwerte')

# Achsenstart- und endpunkte setzen, falls aktiviert
if Plot_Auto == False:
    plt.xlim(left=plot_x_start, right=plot_x_end)
    plt.ylim(bottom=plot_y_start, top=plot_y_end)


# Fit-Kurve anzeigen, falls aktiviert
coefficients = None
coeff_errors = None
if plot_fit:
    # Fit-Kurve berechnen
    coefficients, cov_matrix = np.polyfit(plot_xdata, plot_ydata, fit_grad, cov=True)
    fit_x = np.linspace(min(plot_xdata), max(plot_xdata), 1000)
    fit_y = np.polyval(coefficients, fit_x)

    # Fit-Kurve plotten
    plt.plot(fit_x, fit_y, 'r--', label=f'Polynomfit {fit_grad}. Ordnung')

    # Unsicherheiten der Koeffizienten berechnen
    coeff_errors = np.sqrt(np.diag(cov_matrix))
    for i, (coeff, error) in enumerate(zip(coefficients, coeff_errors)):
        print(f"Koef. {i}: {coeff:.3} ± {error:.3}")

    # R^2 berechnen
    residuals = plot_ydata - np.polyval(coefficients, plot_xdata)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((plot_ydata - np.mean(plot_ydata))**2)
    r_squared = 1 - (ss_res / ss_tot)

    # R^2 ausgeben
    print(f"$R^2: {r_squared:.5f}$")
    plt.text(0.5, 0.95, f'$R^2 = {r_squared:.5f}$', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='center')

# Plot-Einstellungen
plt.xlabel(plot_xlabel)
plt.ylabel(plot_ylabel)
plt.title(plot_titel)
plt.legend()
plt.grid(True)

# Plot anzeigen
if plot:
    plt.show()

# -------------------------------
# Ergebnisse speichern
# -------------------------------

# Dateiname für die Ergebnisse mit Zeitstempel
Dateiname_Ergebnisse = "Er_" + os.path.basename(__file__).replace('.py', '') + ".txt"

# Ergebnisse in Datei speichern
speichere_ergebnisse(Dateiname_Ergebnisse, messungsnummern,
                     berechnete_ergebnisse, berechnete_fehler, variablen_werte,
                     mittelwert_ergebnis, mittelwert_fehler,
                     standardabweichung, standardfehler_des_mittels, coefficients, coeff_errors)

# Datei nach dem Speichern öffnen (plattformunabhängig)
try:
    if os.name == 'nt':
        os.startfile(os.path.join("Ergebnisse", Dateiname_Ergebnisse))
    elif os.name == 'posix':
        # Für Unix-ähnliche Systeme
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, os.path.join("Ergebnisse", Dateiname_Ergebnisse)])
except Exception as e:
    print(f"Konnte die Datei nicht öffnen: {e}")
