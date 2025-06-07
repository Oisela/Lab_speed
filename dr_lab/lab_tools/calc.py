import numpy as np
import scipy as sp


def gauss_error_product(a, b, da, db):
    """
    Berechnet den Fehler einer Multiplikation a * b mit dem Gaußschen Fehlerfortpflanzungsgesetz.

    Parameter:
    a (float): Wert von a
    b (float): Wert von b
    da (float): absoluter Fehler von a
    db (float): absoluter Fehler von b

    Rückgabe:
    (float, float): Ergebnis der Multiplikation und absoluter Fehler
    """
    result = a * b
    error = result * np.sqrt((da / a)**2 + (db / b)**2)
    return result, error


def gauss_error_propagation(f_derivatives, variables, errors):
    """
    Berechnet die Gaußsche Fehlerfortpflanzung für eine Funktion f(x1, x2, ..., xn).
    
    Parameter:
    - f_derivatives: Liste der partiellen Ableitungen von f nach jeder Variablen (als float-Werte).
    - variables: Liste der Werte der Variablen [x1, x2, ..., xn].
    - errors: Liste der absoluten Fehler [dx1, dx2, ..., dxn].
    
    Rückgabe:
    - Gesamtfehler als float.
    """
    f_derivatives = np.asarray(f_derivatives)
    errors = np.asarray(errors)
    return np.sqrt(np.sum((f_derivatives * errors)**2))


def pythagorean_addition(*errors):
    """
    Führt die pythagoreische Addition mehrerer Fehler durch.
    
    Parameter:
    *errors : float
        Beliebig viele Unsicherheiten (Standardabweichungen), die kombiniert werden sollen.
    
    Rückgabe:
    float
        Die kombinierte Unsicherheit.
    """
    return np.sqrt(np.sum(np.square(errors)))


def weighted_mean_with_error(values, errors):
    """
    Berechnet den gewichteten Mittelwert und die zugehörige Unsicherheit.

    Parameter:
    values : array-like
        Die Messwerte.
    errors : array-like
        Die Unsicherheiten der Messwerte.

    Rückgabe:
    tuple (mean, error)
        Der gewichtete Mittelwert und seine Unsicherheit.
    """
    values = np.array(values)
    errors = np.array(errors)
    
    weights = 1 / errors**2
    mean = np.sum(weights * values) / np.sum(weights)
    error = np.sqrt(1 / np.sum(weights))
    
    return mean, error
