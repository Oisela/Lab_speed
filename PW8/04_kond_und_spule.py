## Version: 1.0$
## Date: 2021-09-29$
## Author: A. Ospelt

# Dieses Programm kann folgende Aufgaben erledigen:
# - Berechnung der Fehlerfortpflanzung für eine gegebene Formel
# - Berechnung des Mittelwerts und der Standardabweichung der Ergebnisse
# - Erstellung eines Plots der Messwerte mit optionaler Fit-Kurve
# - Speichern der Ergebnisse in einer Textdatei

# Die Eingaben erfolgen im Abschnitt "Eingabe" und die Ausgaben werden in den Dateien im Ordner "Ergebnisse" gespeichert.


### 
#
#
# Wichtig alle Variabeln immer in der gleichen Reinenfolge
#
#
###
import csv
import numpy as np
import os  # Für Dateioperationen
import sympy as sp
import subprocess
import sys
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
from datetime import datetime
import math
# -------------------------------
# Funktionen
# -------------------------------
def sience_error(number, significant_digits):
    if number == 0:
        return 0
    elif number > 10:
        return f"{number:.{significant_digits}g}"
    else:
        formatted_number = f"{number:.{significant_digits}g}"
        original_number_str = str(number)
        formetted_length = len(formatted_number)
        if len(original_number_str) - 1 < formetted_length:
            return formatted_number
        else:
            if original_number_str[formetted_length].isdigit() and float(original_number_str[formetted_length]) < 5 and float(original_number_str[formetted_length]) != 0:
                digit_to_increment = int(formatted_number[formetted_length - 1])
                digit_to_increment += 1
                shortened_number = formatted_number[:-1] + str(digit_to_increment)
                return shortened_number
            else:
                return formatted_number

def unsicherheiten_Multimeter(messwert, unsicherheit_prozent, aufloesung, plusterm):
    """
    :Berechnet die Unsicherheit eines Messwertes, der mit einem Multimeter gemessen wurde.
    :param messwert: Messwert
    :param unsicherheit_prozent: Unsicherheit in Prozent (z.B. 0.01 für 1%)
    :param plusterm: Plus-Term integer (z.B. 1 für 0.1)
    :return: Unsicherheit
    """
    unsicherheit = messwert * unsicherheit_prozent
    zusatz =  aufloesung * plusterm
    unsicherheit = unsicherheit + zusatz
    return unsicherheit

def write_to_file(dateipfad, text):
    """
    Schreibt den Text in eine Datei.
    """
    try:
        # Datei im Schreibmodus öffnen, um den neuen Text oben hinzuzufügen
        with open(dateipfad, 'a', encoding='utf-8') as f:
            f.write(text + '\n' )
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

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

def speichere_ergebnisse(dateipfad, messungsnummern, ergebnisse, fehler, variablen_werte):
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
    #def sience_error(number, significant_digits):
    #    if number == 0:
    #        return 0
    #    else:
    #        formatted_number = f"{number:.{significant_digits}g}"
    #        original_number_str = str(number)
    #        formetted_length = len(formatted_number)
    #        if len(original_number_str) - 1  < formetted_length:
    #            return formatted_number
    #        else:  
    #            if int(original_number_str[formetted_length]) < 5 and int(original_number_str[formetted_length]) != 0:
    #                digit_to_increment = int(formatted_number[formetted_length - 1])
    #                digit_to_increment += 1
    #                shortened_number = formatted_number[:-1] + str(digit_to_increment)
    #                return shortened_number
    #            else:
    #                return formatted_number

    with open(dateipfad, 'a', encoding='utf-8') as f:
        # Variablen und deren Werte schreiben
        f.write("Verwendete Variablen und Werte:\n")
        for var_name, var_value in variablen_werte.items():
            f.write(f"{var_name} = {var_value}\n")
        f.write("\n")
        # Header schreiben
        f.write(f"{'Messung':<10}{f'{ergebnis_name} ({ergebnis_einheit})':<20}{f'Fehler ({ergebnis_einheit})':<20}\n")
        # Ergebnisse schreiben
        for i, n, dn in zip(messungsnummern, ergebnisse, fehler):
            f.write(f"{i:<10.{max_signifikante_stellen}g}{n:<20.{max_signifikante_stellen}g}{dn:<20.{max_signifikante_stellen}g}\n")
        # Mittelwerte schreiben
        
        # LaTeX-Formatierung
        if len(ergebnisse) > 1:
            f.write("\n")
            # Ergebnisse schreiben (für LaTeX)
            f.write("Ergebnisse für LaTeX:\n")
            f.write("\n")
            f.write("\\begin{table}[H] \n")
            f.write("\t \\centering \n" )
            f.write("\t \\begin{tabular}{|c|c|} \n")
            f.write(f"\t \t \hline Messungen & {ergebnis_name} (${ergebnis_einheit}$)  \\\ \hline \n")
            for i, n, dn in zip(messungsnummern, ergebnisse, fehler):
                dn = sience_error(dn, Signifikante_Stellen)
                if float(dn) >= 10 or len(dn) == 1:
                    leng_of_error = 0
                else:
                    leng_of_error = len(str(dn).split(".")[1])    # Länge des Fehlers
                f.write(f"\t \t \hline {i} & ${n:.{leng_of_error}f} \pm {dn}$ \\\ \n")
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

def generate_fit_curve_data( plot_xdata, plot_fit2, plot_fit2_grad, plot_fit2_start, plot_fit2_end, plot_ydata, linestyle, dotstyle, y_errors=None, initial_guess=None, fit_function=None):
    """
    Generiert die Daten für die Fit-Kurve und berechnet die Fit-Koeffizienten und deren Unsicherheiten.
    """
    
    plotX_xdata = plot_xdata[plot_fit2_start:plot_fit2_end]
    plotX_ydata = plot_ydata[plot_fit2_start:plot_fit2_end]
    
    if fit_funktion == True and variabeln_fit == 1:
        # Fit-Kurve berechnen
        coefficients, cov_matrix = curve_fit(fit_funktion_Def, plotX_xdata, plotX_ydata, sigma=y_errors)
        fit2_x = np.linspace(min(plotX_xdata), max(plotX_xdata), 1000)
        fit2_y = fit_funktion_Def(fit2_x, *coefficients)
        plt.plot(fit2_x, fit2_y, linestyle, label=f'Curve-Fit {fit_function_name}')
        residuals = plotX_ydata - fit_funktion_Def(plotX_xdata, *coefficients)
    elif fit_funktion == True and variabeln_fit == 2:
        coefficients, cov_matrix = curve_fit(fit_funktion_Def, plotX_xdata, plotX_ydata, p0=initial_guess, sigma=y_errors)
        fit2_x = np.linspace(min(plotX_xdata), max(plotX_xdata), 1000)
        fit2_y = fit_funktion_Def(fit2_x, *coefficients)
        plt.plot(fit2_x, fit2_y, linestyle, label=f'Curve-Fit {fit_function_name}')
        residuals = plotX_ydata - fit_funktion_Def(plotX_xdata, *coefficients)
    
    elif fit_funktion == False:
        coefficients, cov_matrix = np.polyfit(plotX_xdata, plotX_ydata, plot_fit2_grad, cov=True)
        fit2_x = np.linspace(min(plotX_xdata), max(plotX_xdata), 1000)
        fit2_y = np.polyval(coefficients, fit2_x)
        plt.plot(fit2_x, fit2_y, linestyle, label=f'Polynomfit {plot_fit2_grad}. Ordnung')
        residuals = plotX_ydata - np.polyval(coefficients, plotX_xdata)
    print(f"Fit-Koeffizienten: {coefficients}")
    # Unsicherheiten der Koeffizienten berechnen
    coeff_errors = np.sqrt(np.diag(cov_matrix))
    for i, (coeff, error) in enumerate(zip(coefficients, coeff_errors)):
        print(f"Koef. {i}: {coeff:.3} ± {error:.3}")

    # R^2 berechnen
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((plotX_ydata - np.mean(plotX_ydata))**2)
    r2_squared = 1 - (ss_res / ss_tot)

    # R^2 ausgeben
    print(f"$R^2 Plot-Fit 2: {r2_squared:.5f}$")
    plt.plot([], [], dotstyle, label=f"$R^2 = {r2_squared:.5f}$")
    if coefficients is not None:
        text = f"Fit-Koeffizienten Fit {linestyle}:\n"
        for i, (coeff, error) in enumerate(zip(coefficients, coeff_errors)):
            text += (f"Koef. {i}: {coeff:.{max_signifikante_stellen}g} ± {error:.{max_signifikante_stellen}g}\n")
        text += "\n"
    # R2 Latex
    text += "Latex R^2:"
    text += "\n"
    text += "\\begin{align*} \n"
    text += f"\t R^2 &= {r2_squared:.5g} \n"
    text += "\\end{align*} \n"
    text += "\n"
    latex_ergebnisse(dateipfad, coefficients, coeff_errors)
    write_to_file(dateipfad, text)

def latex_ergebnisse(dateipfad, ergebnisse, fehler):
    with open(dateipfad, 'a', encoding='utf-8') as f:
        f.write("Ergebnisse für LaTeX:\n")
        f.write("\n")
        f.write("\\begin{align*} \n")
        for e, err in zip(ergebnisse, fehler):
            f.write(f"\t ? &= \\SI{{{e:.{Signifikante_Stellen+1}g}({err:.{Signifikante_Stellen+1}g})}}{{{ergebnis_einheit}}} \n" )
        f.write("\\end{align*} \n")
        f.write("\n")

def cvsimport(file, delimiter, skip_header):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        if skip_header:
            next(reader, None)  # Skip the header row
        data = list(reader)
    return data

def calculate_scaled_results_error(anzahl_messungen, skalierung, formel, variablen, messwerte, fehler ):
    for i in range(anzahl_messungen):
        # Ergebnis und Fehler berechnen
        ergebnis, gesamtfehler = fehlerfortpflanzung(formel, variablen, messwerte[i], fehler[i])

        # Ergebnis skalieren
        ergebnis_skaliert = ergebnis * skalierung
        gesamtfehler_skaliert = gesamtfehler * skalierung

        # Zu Listen hinzufügen
        berechnete_ergebnisse.append(ergebnis_skaliert)
        berechnete_fehler.append(gesamtfehler_skaliert)
    return berechnete_ergebnisse, berechnete_fehler

def calculate_weighted_mean(Gewichteter_mean_error, berechnete_ergebnisse, berechnete_fehler, NR):
    if Gewichteter_mean_error:
        gewichtungsfaktor = 1 / np.array(berechnete_fehler)**2
        mittelwert_gewichtet = np.sum(gewichtungsfaktor * berechnete_ergebnisse) / np.sum(gewichtungsfaktor)
        fehler_mittelwert_gewichtet = 1 / np.sqrt(np.sum(gewichtungsfaktor))
        # Ergebnisse schreiben
        text = "\n"
        text +=f"Gewichteter Mittelwert {NR}: {mittelwert_gewichtet:.{max_signifikante_stellen}g} {ergebnis_einheit}\n"
        text +=f"Fehler des gewichteten Mittelwerts {NR}: {fehler_mittelwert_gewichtet:.{max_signifikante_stellen}g} {ergebnis_einheit}\n"
        text += "\n"
        write_to_file(dateipfad, text)

    else:
        mittelwert_gewichtet = None
        fehler_mittelwert_gewichtet = None
    return mittelwert_gewichtet,fehler_mittelwert_gewichtet

def plot_data_with_error(plot_error, plot_xdata, plot_ydata, berechnete_fehler, error_X=None, desing='bo', Name='Messwerte'):
    if plot_error:
        plt.errorbar(plot_xdata, plot_ydata, yerr=berechnete_fehler, xerr=error_X, fmt=desing, label=Name, capsize=5)
    else:
        plt.plot(plot_xdata, plot_ydata, desing, label=Name)

# -------------------------------
# Variablendefinitionen
# -------------------------------h
Nr2_Daten = False
Nr2_calculate = False
Nr2_skalierung =   1
Nr2_anzahl_messungen = 8
Nr2_gewichteter_mean_error = False

Nr3_Daten = False
Nr3_calculate = False
Nr3_skalierung =   1
Nr3_anzahl_messungen = 8
Nr3_gewichteter_mean_error = False

calculate = True # Berechnung der Ergebnisse
Gewichteter_mean_error = False
anzahl_messungen = 21  # Kann leicht angepasst werden
skalierung =   1  # Skalierungsfaktor für die Ergebnisse (z.B. 1000 für mPa·s)
ergebnis_einheit = r'\henry'  # Einheit des Ergebnisses no latex needed
ergebnis_name = r'Wiederstand Spule'  # Name des Ergebnisses
Signifikante_Stellen = 2    # Anzahl der signifikanten Stellen
max_signifikante_stellen = 10 # Maximale Anzahl der signifikanten Stellen
# Hier kannst du alle Variablen und Konstanten definieren, die du benötigst
R, omega, U_C, U_0  = sp.symbols('R omega U_C U_0')

# Formel mit SymPy-Funktionen definieren
formel =  U_C / U_0

# Definiere die Variablen als String (Reihenfolge muss mit den Daten übereinstimmen)
variablen = 'R omega U_C U_0'

# Konstanten (für alle Messungen gleich)
#daten = cvsimport(os.path.join(os.path.dirname(__file__), '2031.csv'), ',', True)
R = 25.6
omega = np.array([
    3142,
    3770,
    4398,
    5027,
    5655,
    6283,
    6912,
    7540,
    8168,
    8796,
    9425,	
    10053,
    10681,
    11310,
    11938,
    12566,
    13195,
    13823,
    14451,
    15080,
    15708
])
error_R = 0.6
error_omega = np.array([13] * anzahl_messungen)

U_C = np.array([
1.132,
1.194,
1.265,
1.331,
1.379,
1.403,
1.397,
1.360,
1.291,
1.190,
1.062,
0.919,
0.788,
0.677,
0.588,
0.518,
0.460,
0.413,
0.372,
0.338,
0.309
])
U_0 = np.array([
0.975,
0.948,
0.906,
0.846,
0.772,
0.688,
0.612,
0.550,
0.513,
0.506,
0.531,
0.587,
0.652,
0.708,
0.752,
0.785,
0.809,
0.827,
0.842,
0.853,
0.862
])

error_U_C = []
error_U_0 = []
for i in range(anzahl_messungen):
    error_L = unsicherheiten_Multimeter(U_C[i], 0.01, 0.001, 3)
    error_X = unsicherheiten_Multimeter(U_0[i], 0.01, 0.001, 3)
    error_U_C.append(error_L)
    error_U_0.append(error_X)
# From 

# Variablen und deren Werte sammeln für text 
variablen_werte = {
    'R': R,
    'omega': omega,
    'U_c': U_C,
    'U_0': U_0,
    'error_R': error_R,
    'error_omega': error_omega,
    'error_U_C': error_U_C, 
    'error_U_0': error_U_0
}

# Werte für jede Variable
# Verwende [i] für die Indizierung, um die Werte für jede Messung zu speichern


## Reihenfolge beachten ##
messwerte = [
    [R, omega[i], U_C[i], U_0[i]] for i in range(anzahl_messungen) 
]
# Fehler für jede Variable
fehler = [
    [error_R, error_omega[i], error_U_C[i], error_U_0[i]] for i in range(anzahl_messungen)
]
messungsnummern = list(range(1, anzahl_messungen + 1))
#
### Messwerte 2
if Nr2_Daten:
    Nr2_messwerte = [
    [R2[i], V2_Aus[i]] for i in range(anzahl_messungen) 
    ]
    # Fehler für jede Variable
    Nr2_fehler = [
        [error_r2[i], error_V2[i]] for i in range(anzahl_messungen)
        ]
    messungsnummern = list(range(1, anzahl_messungen + 1))
#
### Messwerte 3
if Nr3_Daten:
    Nr3_messwerte = [
    [R[i], V_Aus[i]] for i in range(anzahl_messungen) 
    ]
    # Fehler für jede Variable
    Nr3_fehler = [
        [error_r[i], error_V[i]] for i in range(anzahl_messungen)
        ]



# Plot Einstellungen
plot = True     
change_data = False                           # Plot erstellen
plot_xlabel = r'Kreisfrequenz $\omega$ in $s^{-1}$ '                 # Beschriftung der x-Achse
plot_ylabel = r'$X_L$ in $\Omega$ '      # Beschriftung der y-Achse
plot_titel  = r'' # Titel des Plots
plot_error = True                # Fehlerbalken im Plot anzeigen
plot_xdata = omega  # x-Achse: wenn Messungezahal, dann : Messungsnummern if False dann ergebnisse
plot_ydata = None  # y-Achse: Messwerte if False dann ergebnisse
plot_xerror = error_omega
plot_yerror = None
plot_data_name = r'Messwerte'

Nr2_plot_data = False
Nr2_plot_error = False
Nr2_plot_ydata = None     # if False dann ergebnisse
Nr2_plot_xdata = None         # if False dann Messungsnummern
Nr2_plot_xerror = None
Nr2_plot_yerror = None
Nr2_plot_data_name = r'Messwerte bei $V4$'

Nr3_plot_data = False
Nr3_plot_error = False
Nr3_plot_ydata = False
Nr3_plot_xdata = False
Nr3_plot_xerror = None
Nr3_plot_yerror = None
Nr3_plot_data_name = 'Messwerte 3'

## Plot Fit Einstellungen
plot_fit = True                  # Fit-Kurve im Plot anzeigen
fit_grad = 3                         # Hier den gewünschten Grad des Fits angeben
fit_funktion = True    # Hier die gewünschte Fit-Funktion angeben if true curve_fit if false polyfit
fit_function_name = r'$\frac{1}{\omega \cdot C}$'
variabeln_fit = 2
initial_guess = [10000, 500]
#Fit funktion definieren
def fit_funktion_Def(omega, omega_0, delta):
    return (omega_0**2) / np.sqrt((omega_0**2 - omega**2)**2 + 4 * delta**2 * omega**2)

plot_fit1 = False
if plot_fit1:
    plot_fit1_grad = 1
    plot_fit1_start = None
    plot_fit1_end = None
    plot_fit1_xdata = None
    plot_fit1_ydata = None


plot_fit2 = False
if plot_fit2:
    plot_fit2_grad = 1
    plot_fit2_start = None
    plot_fit2_end = None
    plot_fit2_xdata = False
    plot_fit2_ydata = False


# Variablen für den Start- und Endpunkt der x- und y-Achse und die Option, dies zu aktivieren
Plot_Auto = True
plot_start_at_zero = True
plot_x_start = 0.4 # Startpunkt der x-Achse (None bedeutet automatisch)
plot_x_end = 3.2  # Endpunkt der x-Achse (None bedeutet automatisch)
plot_y_start = 0.004   # Startpunkt der y-Achse (None bedeutet automatisch)
plot_y_end = 0.013 # Endpunkt der y-Achse (None bedeutet automatisch)


##################
## Eingabe Ende ##
##################

if Nr2_plot_data == False:
    Nr2_plot_error = False

if Nr3_plot_data == False:
    Nr3_plot_error = False

if plot == False:
    plot_error = False
    plot_fit = False
    plot_start_at_zero = False
    change_data = False

if Plot_Auto == True:
    plot_start_at_zero = False
    plot_x_start = None
    plot_x_end = None
    plot_y_start = None
    plot_y_end = None   

if plot_fit1 == False:
    plot_fit1_xdata = False
    plot_fit1_ydata = False
if plot_fit2 == False:
    plot_fit2_xdata = False
    plot_fit2_ydata = False

if Nr2_Daten == False:
    Nr2_calculate = False
    Nr2_gewichteter_mean_error = False


if Nr3_Daten == False:
    Nr3_calculate = False
    Nr3_gewichteter_mean_error = False

# -------------------------------
# Berechnungen durchführen
# -------------------------------

# Listen zur Speicherung der berechneten Ergebnisse und Fehler
berechnete_ergebnisse = []
berechnete_fehler = []
Nr2_berechnete_ergebnisse = []
Nr2_berechnete_fehler = []
Nr3_berechnete_ergebnisse = []
Nr3_berechnete_fehler = []


# Dateiname für die Ergebnisse mit Zeitstempel
Dateiname_Ergebnisse = "Er_" + os.path.basename(__file__).replace('.py', '') + ".txt"
ordner = os.path.join(os.path.dirname(__file__), "Ergebnisse")
if not os.path.exists(ordner):
    os.makedirs(ordner)
# Pfad zur Datei im "Ergebnisse" Ordner
dateipfad = os.path.join(ordner, Dateiname_Ergebnisse)
open(dateipfad, 'w').close()  # Datei leeren
# Aktuelles Datum und Uhrzeit ermitteln
aktuelles_datum_zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Datum und Uhrzeit in die Datei schreiben
write_to_file(dateipfad, f"Datum und Uhrzeit der Berechnung: {aktuelles_datum_zeit}\n\n")

# Schleife über jede Messung




if calculate:
    berechnete_ergebnisse, berechnete_fehler = calculate_scaled_results_error(anzahl_messungen, skalierung, formel, variablen, messwerte, fehler)
else: 
    berechnete_ergebnisse = plot_ydata
if Nr2_calculate:
    Nr2_berechnete_ergebnisse, Nr2_berechnete_fehler = calculate_scaled_results_error( Nr2_anzahl_messungen, Nr2_skalierung, formel, variablen, Nr2_messwerte, Nr2_fehler )
else:
    Nr2_berechnete_ergebnisse = Nr2_plot_ydata
if Nr3_calculate:
    Nr3_berechnete_ergebnisse, Nr3_berechnete_fehler = calculate_scaled_results_error( Nr3_anzahl_messungen, Nr3_skalierung, formel, variablen, Nr3_messwerte, Nr3_fehler)
else:
    Nr3_berechnete_ergebnisse = Nr3_plot_ydata

# -------------------------------
# Mittelwerte und Statistiken berechnen
# -------------------------------

# Mittelwert der Ergebnisse und Fehler berechnen
if Gewichteter_mean_error:
    mittelwert_gewichtet, fehler_mittelwert_gewichtet = calculate_weighted_mean(Gewichteter_mean_error, berechnete_ergebnisse, berechnete_fehler, 1)
if Nr2_gewichteter_mean_error:
    Nr2_mittelwert_gewichtet, Nr2_fehler_mittelwert_gewichtet = calculate_weighted_mean(Gewichteter_mean_error, Nr2_berechnete_ergebnisse, Nr2_berechnete_fehler, 2)
if Nr3_gewichteter_mean_error:
    Nr3_mittelwert_gewichtet, Nr3_fehler_mittelwert_gewichtet = calculate_weighted_mean(Gewichteter_mean_error, Nr3_berechnete_ergebnisse, Nr3_berechnete_fehler, 3)

 


# Standardabweichung und Standardfehler des Mittels berechnen (wenn mehr als eine Messung)
if anzahl_messungen > 1:
    standardabweichung = np.std(berechnete_ergebnisse, ddof=1)
    standardfehler_des_mittels = standardabweichung / np.sqrt(anzahl_messungen)
else:
    standardabweichung = None
    standardfehler_des_mittels = None

### Plot erstellen
if change_data:
    temp_plot_xdata = plot_ydata
    temp_plot_ydata = plot_xdata
    plot_xdata = temp_plot_xdata
    plot_ydata = temp_plot_ydata

plt.figure(figsize=(10, 6))


if plot:
    plot_data_with_error( plot_error, plot_xdata, berechnete_ergebnisse, berechnete_fehler, plot_xerror, desing ='bo', Name= plot_data_name )
if Nr2_plot_data:
    plot_data_with_error( Nr2_plot_error, Nr2_plot_xdata, Nr2_berechnete_ergebnisse, Nr2_berechnete_fehler, Nr2_plot_xerror, desing ='ro', Name= Nr2_plot_data_name )
if Nr3_plot_data:
    plot_data_with_error( Nr3_plot_error, Nr3_plot_xdata, Nr2_berechnete_ergebnisse, Nr3_berechnete_fehler, Nr3_plot_xerror, desing ='go',Name= Nr3_plot_data_name )






# Achsenstart- und endpunkte setzen, falls aktiviert
if plot_start_at_zero:
    plt.xlim(left=plot_x_start, right=plot_x_end)
    plt.ylim(bottom=plot_y_start, top=plot_y_end)


# Fit-Kurve anzeigen, falls aktiviert
coefficients = None
coeff_errors = None


#Check for spesicic data for fit
if plot_fit1_xdata is None:
    plot_fit1_xdata = plot_xdata
if plot_fit1_ydata is None:
    plot_fit1_ydata = berechnete_ergebnisse
if plot_fit2_xdata is None:
    plot_fit2_xdata = plot_xdata
if plot_fit2_ydata is None:
    plot_fit2_ydata = berechnete_ergebnisse




if plot_fit == True:
    generate_fit_curve_data(plot_xdata, plot_fit, fit_grad, None, None, berechnete_ergebnisse, 'g--', 'g_', berechnete_fehler)
if plot_fit1 == True:
    generate_fit_curve_data( plot_fit1_xdata, plot_fit1, plot_fit1_grad, plot_fit1_start, plot_fit1_end, plot_fit1_ydata, 'r--', 'r_', berechnete_fehler)
if plot_fit2 == True:
    generate_fit_curve_data( plot_fit2_xdata, plot_fit2, plot_fit2_grad, plot_fit2_start, plot_fit2_end, plot_fit2_ydata, 'b--', 'b_', berechnete_fehler)


# Plot-Einstellungen
plt.xlabel(plot_xlabel)
plt.ylabel(plot_ylabel)
plt.title(plot_titel)
plt.legend()
plt.grid(True)

# Plot anzeigen
if plot:
    #plt.show()
    plotname = dateipfad.replace('.txt', '.png')
    plotname = plotname.replace('Er_', 'Plot_')
    plt.savefig(plotname)
    print(f"Der Plot wurde als '{plotname}' gespeichert.")

speichere_ergebnisse(dateipfad, messungsnummern,
                     berechnete_ergebnisse, berechnete_fehler, variablen_werte)
