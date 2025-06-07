"""
Physics Lab Data Analysis Package

This package provides utilities and functions for analyzing physics lab data,
including data processing, error propagation, plotting, and curve fitting.
"""

# Import submodules to make them available when importing the package
from . import utils
from . import calculation
from . import output
from . import plotting


# Define what gets imported with 'from pylab_def import *'
__all__ = ["utils", "calculation", "output", "plotting" ]
