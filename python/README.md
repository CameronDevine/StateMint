## Python Package

[![Build Status](https://travis-ci.org/CameronDevine/StateMintum.svg?branch=master)](https://travis-ci.org/CameronDevine/StateMintum)
[![PyPI](https://img.shields.io/pypi/v/StateMintum-Py.svg)](https://pypi.org/project/StateMintum-Py/)
[![Documentation Status](https://readthedocs.org/projects/statemintum/badge/?version=latest)](https://statemintum.readthedocs.io/en/latest/?badge=latest)

The StateMintum Python package is an implementation based on [SymPy](http://www.sympy.org) which allows this code to easily combined with simulation and analysis code, or integrated into other systems.
The package provides a `Solve` function which takes the input variables, state variable elemental equations, non-state variable elemental equations, constraint equations, and output variables and returns a Python object with multiple forms of the solution.
These outputs can be further analyzed with SymPy or converted to Numpy objects for easy simulation or numerical analysis.
The full documentation for the code is available on [readthedocs.io](https://statemintum.readthedocs.io/en/latest/).
An [example](https://github.com/CameronDevine/StateMintum/blob/master/python/Example.ipynb) Jupyter notebook is also included with the package.
Because this package is available on PyPI the latest release can be easily installed by running `pip install StateMintum-Py`.
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjAzMjYwNTkzNl19
-->