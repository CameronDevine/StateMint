---
title: 'StateMint: A set of Tools for Determining Symbolic Dynamic System Models using Linear Graph Methods'
tags:
  - system dynamics
  - calculator
  - symbolic math
  - computer algebra system
authors:
  - name: Cameron Devine
    orcid: 0000-0002-6579-111X
    affiliation: 1
  - name: Joseph L. Garbini
    affiliation: 1
  - name: Rico A. R. Picone
    orcid: 0000-0002-5091-5175
    affiliation: "2, 1"
affiliations:
  - name: University of Washington, Department of Mechanical Engineering
    index: 1
  - name: Saint Martin's University, Department of Mechanical Engineering
    index: 2
date: 26 September 2018
bibliography: paper.bib
---

# Abstract

StateMint is a set of software tools that reduce sets of dynamic equations and their constraints to a state-space model and related dynamic system model formulations.
These tools are especially useful for the student of system dynamics, many of whom can become lost in this algebraic reduction.
StateMint includes a Mathematica package, a Python package, and a web interface that is built as a layer on top of the Python package.

# Introduction

When deriving a system's state-space model&mdash;that is, its vector state (differential) equation and its vector output (algebraic) equation&mdash;one begins by forming one (or more) scalar equation for each element describing its dynamics.
The next step is to form a set of N constraint equations that describe the topology of the system defined by the interconnection of the N elements.
A set of 2N differential and algebraic equations and 2N unknown variables results.
If properly constructed (e.g. with the linear graph technique), N of the unknown variables can be immediately eliminated through direct substitution.
Finally, the set of equations can be reduced to a system of first-order differential equations in state and input variables and their time-derivatives, alone.
It is in these last two steps, especially the very last, that a student manually reducing the set of equations will often make some minor mistake, typically of a "book keeping" variety that, if it teaches the student anything, it is not system dynamics.
Instead, the student can be easily discouraged and confused about where they have made their mistake.
Fortunately, this process can be automated with the software tools presented here.
These will allow students to focus on understanding the process of dynamic system modeling.

Utilizing the advanced symbolic mathematics capabilities of Mathematica, a package was written to determine the dynamic system model.
However, this requires students to purchase, install, and learn Mathematica, often with a considerable monetary investment and a learning curve.
To mitigate these problems, a web app was designed to allow students to use this tool without any knowledge of programming by allowing equations to be input in BASIC notation, similar to most scientific calculators.
To support this interface, a Python package was written with the same functionality as the Mathematica package and is deployed by the web app as an Amazon AWS Lambda function.
This app can be accessed by any device with an internet connection and a web browser.

# Web Interface

The [web interface](http://statemint.camerondevine.me/) has text boxes for entering equations and variables.
A special form of the constraint equations is required, as described in the tutorial, based on the work of Rowell and Wormley [@rowell1997].
Once entered, the equations are sent to the Lambda function and the dynamic system model is returned.
The results are then displayed as rendered math or source code in any of the following languages: \LaTeX, Matlab, Python, and Mathematica.
Examples and documentation are built-in, allowing the user to learn the interface as they use it.
The user input can be shared, downloaded, and saved for later use or modification.
Because this interface utilizes Amazon AWS serverless resources, required maintenance and costs are minimized.
An automated installer for independent deployment of the website is also [included](https://github.com/CameronDevine/StateMint/tree/master/web) in the StateMint repository.

# Python Package

The Python package uses the SymPy [@meurer2017] library to symbolically reduce the set of elemental and constraint equations to the state and output equations.
This function returns an object which includes the resulting system as a state-space model, a transfer function, and an equation.
Helper functions are included to convert the symbolic matrices to Numpy [@oliphant2015] objects.
This code is documented using [readthedocs.io](https://statemint.readthedocs.io/en/latest/) and works for both linear and nonlinear systems.

An example of how to use this package is [included](https://github.com/CameronDevine/StateMint/blob/master/python/Example.ipynb).

# Mathematica Package

The Mathematica package `StateMint` can be installed as described in the [documentation](https://github.com/CameronDevine/StateMint/blob/master/mathematica/README.md). The central function of the package is `stateEquations`, which uses an algorithm similar to that of the Python package, above, to derive the state equations. It takes as arguments lists of elemental equations, constraint equations, primary variables, and input variables and returns the vector state equation, state variables, and the time-derivative of the state variables.

The `outputEquations` function derives the output equations given output expressions in terms of primary and secondary variables (including inputs). The function accepts lists of input variables, state variables, elemental and constraint equations, and output expressions.

The functions `stateEquations` and `outputEquations` yield what are in general *nonlinear* state and output equations. Linear state and output equations are typically written in a standard vector form described by matrices `A`, `B`, `C`, and `D` (and sometimes `E` and `F`). The `linearizeState` function accepts lists of input variables, state variables, and the time-derivatives of the state vector (from `stateEquations`) and returns the `A`, `B`, and `E` matrices. Similarly, `linearizeOutput` returns the `C`, `D`, and `F` matrices.

An example of how to use this package is [included](https://github.com/CameronDevine/StateMint/blob/master/mathematica/Example.nb).

# Acknowledgments

The authors would like to acknowledge the work of [Gavin Basuel](https://www.gavinbasuel.com/) who designed the user experience for the web interface and helped with HTML/CSS development.

# References

<!--stackedit_data:
eyJkaXNjdXNzaW9ucyI6eyJ2QWlBMUtnQUJta1lPY01lIjp7In
RleHQiOiJCQVNJQyBub3RhdGlvbiIsInN0YXJ0IjoyODY1LCJl
bmQiOjI4Nzl9LCJsdmNEODBUSHYyUTlLTVQ3Ijp7InN0YXJ0Ij
ozMzg3LCJlbmQiOjMzOTUsInRleHQiOiJ0dXRvcmlhbCJ9LCJ0
dG5oaFpxdjhqekRqemtlIjp7InN0YXJ0IjozOTg1LCJlbmQiOj
QxNTcsInRleHQiOiJBbiBhdXRvbWF0ZWQgaW5zdGFsbGVyIGZv
ciBpbmRlcGVuZGVudCBkZXBsb3ltZW50IG9mIHRoZSB3ZWJzaX
RlIGlzIGFsc28gW2luY2x14oCmIn0sIkc3SnhoWkpHZVV6Um9o
SE8iOnsic3RhcnQiOjQ0MTAsImVuZCI6NDQyMSwidGV4dCI6In
N0YXRlLXNwYWNlIn19LCJjb21tZW50cyI6eyJFdU9VdmJGaUg1
cVRuS1EwIjp7ImRpc2N1c3Npb25JZCI6InZBaUExS2dBQm1rWU
9jTWUiLCJzdWIiOiJnaDoxMDM5NDg5NiIsInRleHQiOiJTaG91
bGQgd2UgY2l0ZSBCQVNJQyBub3RhdGlvbj8gSSBmb3VuZCBpdC
BvbiBXaWtpcGVkaWEsICBcbltodHRwczovL2VuLndpa2lwZWRp
YS5vcmcvd2lraS9DYWxjdWxhdG9yX2lucHV0X21ldGhvZHMjQk
FTSUNfbm90YXRpb25dKGh0dHBzOi8vZW4ud2lraXBlZGlhLm9y
Zy93aWtpL0NhbGN1bGF0b3JfaW5wdXRfbWV0aG9kcyNCQVNJQ1
9ub3RhdGlvbikiLCJjcmVhdGVkIjoxNTQzOTUzNzU0NjQ5fSwi
RVVENlpFWUtzT1pZQVdxZiI6eyJkaXNjdXNzaW9uSWQiOiJ2QW
lBMUtnQUJta1lPY01lIiwic3ViIjoiZ286MTAyOTA1NDM1NTMw
ODk2NDc0ODAwIiwidGV4dCI6IkkgdGhpbmsgdGhhdCB3b3VsZC
BiZSBnb29kIHRvIGNpdGUgaXQgLi4uIEJBU0lDIGlzIGEgbGFu
Z3VhZ2UsIHJpZ2h0PyBTbyBJJ2QgY2l0ZSBpdCBob3dldmVyIH
lvdSd2ZSBiZWVuIGNpdGluZyB0aGUgb3RoZXJzIC4uLiIsImNy
ZWF0ZWQiOjE1NDQ1MTYyNjEzNzV9LCJKSjV3UE9LUVd4VEswUF
V1Ijp7ImRpc2N1c3Npb25JZCI6Imx2Y0Q4MFRIdjJROUtNVDci
LCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZX
h0IjoiaHJlZiIsImNyZWF0ZWQiOjE1NDQ1NTcyOTMyMjh9LCJo
WkJLT1l5ZzhRbVRNT3JxIjp7ImRpc2N1c3Npb25JZCI6InR0bm
hoWnF2OGp6RGp6a2UiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4
OTY0NzQ4MDAiLCJ0ZXh0IjoiRGlkIEkgcHJvcGVybHkgY2xhcm
lmeSB0aGlzPyIsImNyZWF0ZWQiOjE1NDQ1NTczMjk3NDJ9LCJh
SmU2R0JZNWxpUWNuSVlmIjp7ImRpc2N1c3Npb25JZCI6InR0bm
hoWnF2OGp6RGp6a2UiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4
OTY0NzQ4MDAiLCJ0ZXh0IjoiQWxzbywgZG9lcyBpdCBhbGxvdy
Bzb21lb25lIHRvIGhvb2sgdXAgdGhlaXIgb3duIEFXUyBpbnN0
YW5jZSAuLi4gYW5kIGRpZCB5b3UgaW5jbHVkZSBkb2NzIG9uIG
hvdyB0byBnZXQgdGhlIEFXUyBzZXQgdXA/IiwiY3JlYXRlZCI6
MTU0NDU1NzM4NzkyOH0sImlsMXRPalM3NTFOOVFXaFYiOnsiZG
lzY3Vzc2lvbklkIjoiRzdKeGhaSkdlVXpSb2hITyIsInN1YiI6
ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOiJXZS
BzaG91bGQgZG91YmxlIGNoZWNrIHRoYXQgd2UncmUgY29uc2lz
dGVudGx5IGh5cGhlbmF0aW5nIHN0YXRlLXNwYWNlIC4uLiBpdC
dzIHRoZSBzdGFuZGFyZCB1c2FnZSIsImNyZWF0ZWQiOjE1NDQ1
NTg2Njc4OTd9fSwiaGlzdG9yeSI6WzgwMTU1Nzk2MywtMTY4Mz
Q2OTQ0OSwtMTE3MTUwOTc5OSwtMjY3NzY2Mzk1LC01NTY5NDAz
MDcsNDMzNzQ0NjkzLC0zODc1MzI5MjAsMzIzMzI2Njg0LDUxMj
YwOTU5NiwtMTk0OTQxMzYwMiwtNDIyMDQxNTk1LC0xNjU1NTY4
NDE0LC0xMjA5NzUwNzk2LC03MzU2MDU0NjUsMTcxNzIwMDA4Ni
wtMTUxMzkwNTAwNywyMDIyMjk1Mzc3LC05MjA5Njk2NjMsODc0
NDAyMTkxLDUyMDIwNzE1NF19
-->