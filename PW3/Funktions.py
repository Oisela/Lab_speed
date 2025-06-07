import sympy as sp
import numpy as np
import os
import sys
import csv


sys.path.append(os.path.abspath('../Master_Labor/Funktions.py'))


# Funktion zum Einlesen der Daten aus einer Datei
def read_data(filename, t_list, x_list, y_list ):
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=';')

            # Überspringe die erste Zeile, wenn sie Kommentare enthält
            next(reader)  # Überspringt die Kopfzeile

            # Daten lesen
            #for row in reader:
            for index, row in enumerate(reader):
                if index % 1 == 0:  # Nur jede zweite Zeile (Index 0, 2, 4, ...)
                    t_list.append(float(row[0]))
                    x_list.append(float(row[1]))
                    y_list.append(float(row[2]))
    except FileNotFoundError:
        print(f"Die Datei '{filename}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Es ist ein Fehler aufgetreten: {e}")

def speichere_ergebnisse(dateiname, messungsnummern, viskositaeten, fehler, variablen_werte,
                         mittelwert_viskositaet, mittelwert_fehler,
                         standardabweichung=None, standardfehler=None):
    """
    Speichert die Ergebnisse in eine Textdatei, überschreibt bestehende Daten.
    Fügt die verwendeten Variablen und deren Werte hinzu sowie den Mittelwert und den mittleren Fehler.

    Args:
        dateiname (str): Name der Datei, in die die Ergebnisse gespeichert werden.
        messungsnummern (list of int): Liste der Messungsnummern.
        viskositaeten (list of float): Liste der berechneten Viskositäten.
        fehler (list of float): Liste der berechneten Fehler.
        variablen_werte (dict of str: float): Dictionary mit Variablennamen und deren Werten.
        mittelwert_viskositaet (float): Mittelwert der Viskositäten.
        mittelwert_fehler (float): Mittelwert der Fehler.
        standardabweichung (float, optional): Standardabweichung der Viskositäten.
        standardfehler (float, optional): Standardfehler des Mittels.
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
            for i, n, dn in zip(messungsnummern, viskositaeten, fehler):
                f.write(f"{i:<10}{n:<20.5f}{dn:<20.5f}\n")

            # Mittelwerte schreiben
            f.write("\n")
            f.write(f"Mittelwert der {ergebnis_name}: {mittelwert_viskositaet:.5f} {ergebnis_einheit}\n")
            f.write(f"Mittelwert der Fehler: {mittelwert_fehler:.5f} {ergebnis_einheit}\n")

            # Optional: Standardabweichung und Standardfehler des Mittels schreiben
            if standardabweichung is not None:
                f.write(f"Standardabweichung: {standardabweichung:.5f} {ergebnis_einheit}\n")
            if standardfehler is not None:
                f.write(f"Standardfehler des Mittels: {standardfehler:.5f} {ergebnis_einheit}\n")

        print(f"Die Ergebnisse wurden in die Datei '{dateipfad}' geschrieben.")
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





