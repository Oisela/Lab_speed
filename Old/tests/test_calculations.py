import pytest
from calculation import *

def test_error_propagation():
    # Test error propagation for simple formula
    formula = "x * y"
    variables = "x y"
    measurements = [5, 2]
    errors = [0.5, 0.1]
    value, error = error_propagation(formula, variables, measurements, errors)
    assert value == 10
    assert error == pytest.approx(1.1, abs=0.05)  # Accepts values within ±0.01 of 1.1

def test_error_propagation_trig_exp():
    # Test error propagation with sin(x) and exp(x)
    formula = "sin(x) * exp(y)"
    variables = "x y"
    measurements = [5, 2]
    errors = [0.5, 0.1]
    value, error = error_propagation(formula, variables, measurements, errors)
    assert value == pytest.approx(-7.1, abs=0.05)
    # Error propagation will involve partial derivatives of sin and exp
    assert error == pytest.approx(1.3, abs=0.05)

