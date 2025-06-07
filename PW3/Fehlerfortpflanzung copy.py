import numpy as np
import os  # Für Dateioperationen
import sympy as sp
import subprocess
import sys

# -------------------------------
# Variablendefinitionen
# -------------------------------

# Anzahl der Messungen
anzahl_messungen = 10  # Kann leicht angepasst werden
skalierung = 1  # Skalierungsfaktor für die Ergebnisse (z.B. 1000 für mPa·s)
ergebnis_einheit = 'Newton'  # Einheit des Ergebnisses
ergebnis_name = 'Kraft'  # Name des Ergebnisses

# Definiere die Formel als String
formel = '(m / a) * b'

# Definiere die Variablen als String (Reihenfolge muss mit den Daten übereinstimmen)
variablen = 'm a b'

# Konstanten (für alle Messungen gleich)
a = 9.81
m = 10  # kg

# Absolute Fehler der Konstanten
fehler_a = 0.01  # Fehler bei 'a'
fehler_m = 0.01  # Fehler bei 'm1'

# Messwerte
b = [14, 14, 14 , 14, 13.5, 13.8, 13.8, 13.8, 13.8, 13]
fehler_b = [0.5] * anzahl_messungen  # Absoluter Fehler von 0.4 Sekunden




# Variablen und deren Werte sammeln
variablen_werte = {
    'a (m/s^2)': a,
}

# Werte für jede Variable
# Verwende [i] für die Indizierung, um die Werte für jede Messung zu speichern

messwerte = [
    [m, a, b[i]] for i in range(anzahl_messungen) 
]

# Fehler für jede Variable
fehler = [
    [fehler_m, fehler_a, fehler_b[i]] for i in range(anzahl_messungen)
]

##################
## Eingabe Ende ##
##################



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

import os

import os

def speichere_ergebnisse(dateiname, messungsnummern, ergebnisse, fehler, variablen_werte,
                         mittelwert_ergebnis, mittelwert_fehler,
                         ergebnis_name, ergebnis_einheit,
                         standardabweichung=None, standardfehler=None,
                         tabellen_beschriftung="Messwerttabelle",
                         tabellen_label="tab:messwerte"):
    """
    Speichert die Ergebnisse in eine LaTeX-Datei gemäß einer vorgegebenen Vorlage.
    Fügt die verwendeten Variablen und deren Werte hinzu sowie den Mittelwert und den mittleren Fehler.

    Args:
        dateiname (str): Name der Datei, in die die Ergebnisse gespeichert werden (ohne .tex Endung).
        messungsnummern (list of int): Liste der Messungsnummern.
        ergebnisse (list of float): Liste der berechneten Ergebnisse.
        fehler (list of float): Liste der berechneten Fehler.
        variablen_werte (dict of str: float): Dictionary mit Variablennamen und deren Werten.
        mittelwert_ergebnis (float): Mittelwert der Ergebnisse.
        mittelwert_fehler (float): Mittelwert der Fehler.
        ergebnis_name (str): Name des Ergebnisses (z.B. 'F_q').
        ergebnis_einheit (str): Einheit des Ergebnisses (z.B. 'N').
        standardabweichung (float, optional): Standardabweichung der Ergebnisse.
        standardfehler (float, optional): Standardfehler des Mittels.
        tabellen_beschriftung (str, optional): Beschriftung der Tabelle für die Caption.
        tabellen_label (str, optional): Label der Tabelle für die Referenzierung.
    """
    # Ordner "Ergebnisse" erstellen, falls er nicht existiert
    ordner = "Ergebnisse"
    if not os.path.exists(ordner):
        os.makedirs(ordner)

    # Pfad zur Datei im "Ergebnisse" Ordner, mit .tex Endung
    dateipfad = os.path.join(ordner, dateiname + '.tex')

    try:
        # Datei im Schreibmodus öffnen ('w' für write), um bestehende Daten zu überschreiben
        with open(dateipfad, 'w', encoding='utf-8') as f:
            # LaTeX-Dokument beginnen
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage[utf8]{inputenc}\n")
            f.write("\\usepackage{amsmath}\n")
            f.write("\\usepackage{siunitx}\n")
            f.write("\\usepackage{float}\n")
            f.write("\\begin{document}\n\n")

            # Variablen und deren Werte schreiben
            f.write("\\section*{Verwendete Variablen und Werte}\n")
            f.write("\\begin{itemize}\n")
            for var_name, var_value in variablen_werte.items():
                f.write(f"    \\item ${var_name} = {var_value}$\n")
            f.write("\\end{itemize}\n\n")

            # Tabelle erstellen
            f.write("\\begin{table}[H]\n")
            f.write("    \\centering\n")
            f.write("    \\begin{tabular}{|c||c|c|}\n")
            f.write("    \\hline n & ")
            f.write(f"${ergebnis_name}$ ({ergebnis_einheit}) & ")
            f.write(f"$\\sigma$ ({ergebnis_einheit}) \\\\\n")
            f.write("    \\hline \\hline\n")

            # Ergebnisse schreiben
            for i, n, dn in zip(messungsnummern, ergebnisse, fehler):
                f.write(f"    \\hline {i} & {n} & {dn} \\\\\n")

            # Doppelte Linie und Mittelwerte schreiben
            f.write("    \\hline \\hline\n")
            f.write(f"    $\\overline{{\\textbf{{x}}}}$ & $\\textbf{{{mittelwert_ergebnis}}}$ & {mittelwert_fehler} \\\\\n")
            f.write("    \\hline\n")
            f.write("    \\end{tabular}\n")
            f.write(f"    \\caption{{{tabellen_beschriftung}}}\n")
            f.write(f"    \\label{{{tabellen_label}}}\n")
            f.write("\\end{table}\n\n")

            # Optional: Standardabweichung und Standardfehler des Mittels schreiben
            f.write("\\section*{Statistische Auswertung}\n")
            if standardabweichung is not None:
                f.write(f"Standardabweichung: ${{{standardabweichung}\\,\\si{{{ergebnis_einheit}}}}}$\\\\\n")
            if standardfehler is not None:
                f.write(f"Standardfehler des Mittels: ${{{standardfehler}\\,\\si{{{ergebnis_einheit}}}}}$\\\\\n")

            # Dokument beenden
            f.write("\\end{document}\n")

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

# -------------------------------
# Ergebnisse speichern
# -------------------------------

# Dateiname für die Ergebnisse mit Zeitstempel
Dateiname_Ergebnisse = "Er_" + ergebnis_name + ".txt"

# Ergebnisse in Datei speichern
speichere_ergebnisse(Dateiname_Ergebnisse, messungsnummern,
                     berechnete_ergebnisse, berechnete_fehler, variablen_werte,
                     mittelwert_ergebnis, mittelwert_fehler,
                     standardabweichung, standardfehler_des_mittels)

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
