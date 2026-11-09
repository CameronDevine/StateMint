# StateMint

[![Python package](https://github.com/CameronDevine/StateMint/actions/workflows/python.yml/badge.svg)](https://github.com/CameronDevine/StateMint/actions/workflows/python.yml)
[![PyPI](https://img.shields.io/pypi/v/StateMint.svg)](https://pypi.org/project/StateMint/)
[![License](https://img.shields.io/github/license/CameronDevine/StateMint.svg)](LICENSE)
[![Code of Conduct](https://img.shields.io/badge/contributor%20covenant-v1.4-blue.svg)](CODE_OF_CONDUCT.md)
[![status](http://jose.theoj.org/papers/7caec95b5db5c18d8a14cbc42fef7bb7/status.svg)](http://jose.theoj.org/papers/7caec95b5db5c18d8a14cbc42fef7bb7)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2633330.svg)](https://doi.org/10.5281/zenodo.2633330)

StateMint is a set of tools to symbolically determine the differential equation describing the dynamics of a system.
As inputs these tools take the elemental and constraint equations of a system, in the forms of Rowell and Wormley's *System Dynamics: An Introduction*, chapter 5, and they return the state and output equations, their matrices, and the transfer function.
A [tutorial](tutorial.md) is available which covers how to prepare equations for use with these tools.
See the [changelog](CHANGELOG.md) for what is new in version 3.

### Web Interface

The [web interface](https://ricopic.one/statemint/) needs no installation: it runs the Python package in the browser with [Pyodide](https://pyodide.org).
Systems can be saved in the browser, downloaded as `.rnd` files, or shared as links.
The [web](web) directory holds its source.

### Python

The Python [package](python) is the reference implementation, built on [SymPy](https://www.sympy.org).
Install it with `pip install StateMint`; an [example](python/Example.ipynb) notebook shows how to use it.

```python
import StateMint

sys = StateMint.Solve(
    ['Fs'],                                       # input variables
    ["vm' = Fm/m", "FK' = K*vK"],                 # state-variable elemental equations
    ['FB = B*vB'],                                # other elemental equations
    ['Fm = Fs - FK - FB', 'vK = vm', 'vB = vm'],  # constraint equations
    ['vm', 'FK + FB'])                            # outputs
sys.A, sys.B, sys.C, sys.D
```

### Mathematica

The Mathematica [package](mathematica) was the original implementation of this tool.
An [example](mathematica/Example.nb) of how to use the Mathematica package is provided.
It is no longer maintained; the Python package and the web interface are.

## Contributors

- Cameron Devine, Dept. of Mechanical Engineering, University of Washington: Python Package and Web Interface
- [Rico Picone](https://ricopic.one), Dept. of Mechanical Engineering, Saint Martin's University: Mathematica Package Maintenance, 3.0 Revival
- Joseph Garbini, Dept. of Mechanical Engineering, University of Washington: Original Mathematica Package and Web Interface Terminology
- [Gavin Basuel](http://gavinbasuel.com), 1G Media & Design: Web Interface User Experience Design
