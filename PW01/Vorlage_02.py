import numpy as np
import matplotlib.pyplot as plt
import os  # Für Dateioperationen
import sympy as sp
import datetime  # Für Datum und Zeit

# -------------------------------
# Variablendefinitionen
# -------------------------------

# Anzahl der Messungen
anzahl_messungen = 4  # Kann leicht angepasst werden
skalierung = 1000 # Skalierungsfaktor für die Ergebnisse (z.B. 1000 für mPa·s)
ergebnis_einheit = 'mPa·s'  # Einheit des Ergebnisses
ergebnis_name = 'Viskosität'  # Name des Ergebnisses

#Label Plot 
plot_xlabel = 'Messungen'
plot_ylabel = 'Viskosität (mPa·s)'
plot_titel  = 'Viskosität von Wasser bei verschiedenen Temperaturen'

# Definiere die Formel als String
formel = 'a * roh * delta_h * delta_t'

# Definiere die Variablen als String (Reihenfolge muss mit den Daten übereinstimmen)
variablen = 'a roh delta_h delta_t'

# Konstanten (für alle Messungen gleich)
a = 4.2e-7 # Angepasster Wert für 'a' in m²
roh = 997  # Dichte in kg/m³

# Absolute Fehler der Konstanten
fehler_a = (a * 0.2) #  +- 0.8e-7 m² Fehler bei 'a'
fehler_delta_h = 0.005  # +- 0.5 cm Fehler bei 'delta_h' 
fehler_roh = 1  # 0.1% relativer Fehler von 'roh'

#Wasserhöhe berechnen
wasserboden = np.array([2.6, 2.5, 3.3, 3.5])
h1 = np.array([24.65, 24.4, 25.2, 25.2])
h2 = np.array([19.85, 19.7, 20.4, 20.5])
delta_h = ( (h2 - wasserboden) +(h1 - wasserboden) ) / 2 
delta_h = delta_h / 100 # Umrechnung in Meter

# Druchschnitt Temperatur
tp1 = np.array([13.2, 23.1, 34.9, 48.8])
tp2 = np.array([14.4, 23.1, 35.6, 50.8])
delta_tp = (tp1 + tp2) / 2

# Messwerte für 'delta_t' (Zeitmessungen in Sekunden)
delta_h_values = delta_h
delta_t_values = [12.04, 11.12, 10.07, 9.21]
fehler_delta_t_values = [0.4] * anzahl_messungen  # Absoluter Fehler von 0.4 Sekunden
fehler_delta_h_values = [0.005] * anzahl_messungen  # Absoluter Fehler von 0.5 cm


# Variablen und deren Werte sammeln
variablen_werte = {
    'a (m/s^2)': a,
    'roh (kg/m^3)': roh,
    'delta_h (m)': delta_h_values[0],
    'fehler_a': fehler_a ,
    'fehler_roh': fehler_roh,
    'fehler_delta_h': fehler_delta_h,
    'fehler_delta_t': fehler_delta_t_values[0]   # Ein Wert für alle Zeitmessungen
}

# Werte für jede Variable
messwerte = [
    [a, roh, delta_h_values[i], delta_t_values[i]] for i in range(anzahl_messungen)
]

# Fehler für jede Variable
fehler = [
    [fehler_a, fehler_roh, fehler_delta_h, fehler_delta_t_values[i]] for i in range(anzahl_messungen)
]

# Messungsnummern für die Ausgabe
messungsnummern = list(range(1, anzahl_messungen + 1))


#
x_plot_ein = delta_tp

#################### Fertig eingaben ####################


# Überprüfe die Anzahl der Zeitmessungen
if len(delta_t_values) != anzahl_messungen:
    raise ValueError("Die Anzahl der Zeitmessungen stimmt nicht mit 'anzahl_messungen' überein.")

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
    
    # Ergebnis in umrechnen
    ergebnis_skaliert = ergebnis * skalierung  # Angenommen, die Formel gibt Ergebnis in Pa·s
    gesamtfehler_skaliert = gesamtfehler * skalierung  # Fehler skaliert
    
    # Zu Listen hinzufügen
    berechnete_ergebnisse.append(ergebnis_skaliert)
    berechnete_fehler.append(gesamtfehler_skaliert)

# -------------------------------
# Mittelwerte und Statistiken berechnen
# -------------------------------

# Mittelwert der Ergebnisse und Fehler berechnen
mittelwert_ergebnis = np.mean(berechnete_ergebnisse)
mittelwert_fehler = np.mean(berechnete_fehler)

# Standardabweichung und Standardfehler des Mittels berechnen
standardabweichung = np.std(berechnete_ergebnisse, ddof=1)
standardfehler_des_mittels = standardabweichung / np.sqrt(anzahl_messungen)

# -------------------------------
# Ergebnisse speichern
# -------------------------------

# Messungsnummern für die Ausgabe
messungsnummern = list(range(1, anzahl_messungen + 1))

# Dateiname für die Ergebnisse
Dateiname_Ergebnisse = "ER_" + os.path.splitext(os.path.basename(__file__))[0] + ".txt"

# Ergebnisse in Datei speichern
speichere_ergebnisse(Dateiname_Ergebnisse, messungsnummern,
                     berechnete_ergebnisse, berechnete_fehler, variablen_werte,
                     mittelwert_ergebnis, mittelwert_fehler,
                     standardabweichung, standardfehler_des_mittels)

# -------------------------------
# Plotten der Daten mit Fehlerbalken
# -------------------------------

plt.errorbar(x_plot_ein, berechnete_ergebnisse, yerr=berechnete_fehler,
             fmt='o', ecolor='red', capsize=5)
plt.xlabel(plot_xlabel)
plt.ylabel(plot_ylabel)
plt.title(plot_titel)
plt.xticks(x_plot_ein)
plt.grid(True)
plt.show()
