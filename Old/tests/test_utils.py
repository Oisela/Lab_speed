import pytest
from pylab.utils import *

def test_format_scientific_error():
    # Test formatting of scientific notation with different significant digits
    
    assert format_scientific_error(0.120, 2) == "0.12"
    assert format_scientific_error(0.122879494984, 2) == "0.13"
    assert format_scientific_error(0.129, 2) == "0.13"
    assert format_scientific_error(12.5984984, 2) == "13"
    assert format_scientific_error(12.5168464984, 2) == "13"
    assert format_scientific_error(115, 2) == "120"
    assert format_scientific_error(11565, 3) == "11600"
    assert format_scientific_error(-0.12365564684864, 2) == "-0.13"
