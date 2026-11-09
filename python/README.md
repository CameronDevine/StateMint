## Python Package

[![Python package](https://github.com/CameronDevine/StateMint/actions/workflows/python.yml/badge.svg)](https://github.com/CameronDevine/StateMint/actions/workflows/python.yml)
[![PyPI](https://img.shields.io/pypi/v/StateMint.svg)](https://pypi.org/project/StateMint/)
[![Documentation Status](https://readthedocs.org/projects/statemint/badge/?version=latest)](https://statemint.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/camerondevine/StateMint/master?filepath=python%2FExample.ipynb)

The StateMint Python package is an implementation based on [SymPy](https://www.sympy.org) which allows this code to be easily combined with simulation and analysis code, or integrated into other systems.
It requires Python 3.10 or later.
The package provides a `Solve` function which takes the input variables, state variable elemental equations, non-state variable elemental equations, constraint equations, and output variables and returns a Python object with multiple forms of the solution.
These outputs can be further analyzed with SymPy or converted to Numpy objects for easy simulation or numerical analysis.
The full documentation for the code is available on [readthedocs.io](https://statemint.readthedocs.io/en/latest/).
An [example](https://github.com/CameronDevine/StateMint/blob/master/python/Example.ipynb) Jupyter notebook (also available on [binder](https://github.com/CameronDevine/StateMint/blob/master/python/Example.ipynb)) is included with the package.
Because this package is available on PyPI the latest release can be easily installed by running `pip install StateMint`.

Run the tests with `pip install -e ".[test]"` and `pytest` in this directory.
`tests/test_notes_examples.py` checks every worked model in the [System Dynamics notes](https://systems.ricopic.one/).

The Pyodide workflow runs `tests/test_suite.py` in Pyodide using Chromium on
Ubuntu. To run locally:

```sh
pip install -e ".[browser-test]"
python -m playwright install --with-deps chromium
python tests/browser/run_suite.py
```

The runner downloads Pyodide 314.0.7, SymPy, and NumPy from the CDN
and runs the checked-out Python sources, so it requires internet access.
