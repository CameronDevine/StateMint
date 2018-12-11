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
A special form of the constraint equations is required, as described in the [tutorial](https://github.com/CameronDevine/StateMint/blob/master/tutorial.md), based on the work of Rowell and Wormley [@rowell1997].
Once entered, the equations are sent to the Lambda function and the dynamic system model is returned.
The results are then displayed as rendered math or source code in any of the following languages: \LaTeX, Matlab, Python, and Mathematica.
Examples and documentation are built-in, allowing the user to learn the interface as they use it.
The user input can be shared, downloaded, and saved for later use or modification.
Because this interface utilizes Amazon AWS serverless resources, required maintenance and costs are minimized.
An automated installer for independent deployment of the website is also [included](https://github.com/CameronDevine/StateMint/tree/master/web) in the StateMint repository.

# Python Package

The Python package uses the SymPy [@meurer2017] library to symbolically reduce the set of elemental and constraint equations to the state and output equations.
This function returns an object which includes the resulting system as a state-space model, a transfer function, and an equation.
Auxiliary functions are included to convert the SymPy symbolic matrices to Numpy [@oliphant2015] objects.
This package is documented at [readthedocs.io](https://statemint.readthedocs.io/en/latest/) and works for both linear and nonlinear systems.

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
bmQiOjI4Nzl9LCJ0dG5oaFpxdjhqekRqemtlIjp7InRleHQiOi
JBbiBhdXRvbWF0ZWQgaW5zdGFsbGVyIGZvciBpbmRlcGVuZGVu
dCBkZXBsb3ltZW50IG9mIHRoZSB3ZWJzaXRlIGlzIGFsc28gW2
luY2x14oCmIiwic3RhcnQiOjQwNTUsImVuZCI6NDIyN30sIkc3
SnhoWkpHZVV6Um9oSE8iOnsidGV4dCI6InN0YXRlLXNwYWNlIi
wic3RhcnQiOjQ0ODAsImVuZCI6NDQ5MX0sInBMcVpXV0wydXdQ
VkhXekMiOnsidGV4dCI6ImFuIGVxdWF0aW9uIiwic3RhcnQiOj
Q1MjQsImVuZCI6NDUzNX0sIlhaMnU3YnJlTTVOQmZTNlIiOnsi
dGV4dCI6Im9iamVjdHMiLCJzdGFydCI6NDYzNCwiZW5kIjo0Nj
QxfSwiSGh1aXB5M2hmT2pnbm9EUyI6eyJ0ZXh0IjoiVGhpcyBj
b2RlIGlzIGRvY3VtZW50ZWQgYXQgW3JlYWR0aGVkb2NzLmlvXS
hodHRwczovL3N0YXRlbWludC5yZWFkdGhlZG9jcy5pby9lbuKA
piIsInN0YXJ0Ijo0NjQzLCJlbmQiOjQ3ODN9fSwiY29tbWVudH
MiOnsiRXVPVXZiRmlINXFUbktRMCI6eyJkaXNjdXNzaW9uSWQi
OiJ2QWlBMUtnQUJta1lPY01lIiwic3ViIjoiZ2g6MTAzOTQ4OT
YiLCJ0ZXh0IjoiU2hvdWxkIHdlIGNpdGUgQkFTSUMgbm90YXRp
b24/IEkgZm91bmQgaXQgb24gV2lraXBlZGlhLCAgXG5baHR0cH
M6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvQ2FsY3VsYXRvcl9p
bnB1dF9tZXRob2RzI0JBU0lDX25vdGF0aW9uXShodHRwczovL2
VuLndpa2lwZWRpYS5vcmcvd2lraS9DYWxjdWxhdG9yX2lucHV0
X21ldGhvZHMjQkFTSUNfbm90YXRpb24pIiwiY3JlYXRlZCI6MT
U0Mzk1Mzc1NDY0OX0sIkVVRDZaRVlLc09aWUFXcWYiOnsiZGlz
Y3Vzc2lvbklkIjoidkFpQTFLZ0FCbWtZT2NNZSIsInN1YiI6Im
dvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOiJJIHRo
aW5rIHRoYXQgd291bGQgYmUgZ29vZCB0byBjaXRlIGl0IC4uLi
BCQVNJQyBpcyBhIGxhbmd1YWdlLCByaWdodD8gU28gSSdkIGNp
dGUgaXQgaG93ZXZlciB5b3UndmUgYmVlbiBjaXRpbmcgdGhlIG
90aGVycyAuLi4iLCJjcmVhdGVkIjoxNTQ0NTE2MjYxMzc1fSwi
aFpCS09ZeWc4UW1UTU9ycSI6eyJkaXNjdXNzaW9uSWQiOiJ0dG
5oaFpxdjhqekRqemtlIiwic3ViIjoiZ286MTAyOTA1NDM1NTMw
ODk2NDc0ODAwIiwidGV4dCI6IkRpZCBJIHByb3Blcmx5IGNsYX
JpZnkgdGhpcz8iLCJjcmVhdGVkIjoxNTQ0NTU3MzI5NzQyfSwi
YUplNkdCWTVsaVFjbklZZiI6eyJkaXNjdXNzaW9uSWQiOiJ0dG
5oaFpxdjhqekRqemtlIiwic3ViIjoiZ286MTAyOTA1NDM1NTMw
ODk2NDc0ODAwIiwidGV4dCI6IkFsc28sIGRvZXMgaXQgYWxsb3
cgc29tZW9uZSB0byBob29rIHVwIHRoZWlyIG93biBBV1MgaW5z
dGFuY2UgLi4uIGFuZCBkaWQgeW91IGluY2x1ZGUgZG9jcyBvbi
Bob3cgdG8gZ2V0IHRoZSBBV1Mgc2V0IHVwPyIsImNyZWF0ZWQi
OjE1NDQ1NTczODc5Mjh9LCJpbDF0T2pTNzUxTjlRV2hWIjp7Im
Rpc2N1c3Npb25JZCI6Ikc3SnhoWkpHZVV6Um9oSE8iLCJzdWIi
OiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZXh0IjoiV2
Ugc2hvdWxkIGRvdWJsZSBjaGVjayB0aGF0IHdlJ3JlIGNvbnNp
c3RlbnRseSBoeXBoZW5hdGluZyBzdGF0ZS1zcGFjZSAuLi4gaX
QncyB0aGUgc3RhbmRhcmQgdXNhZ2UiLCJjcmVhdGVkIjoxNTQ0
NTU4NjY3ODk3fSwiZEtiUUc4MkRSQ3k0RkZkNCI6eyJkaXNjdX
NzaW9uSWQiOiJwTHFaV1dMMnV3UFZIV3pDIiwic3ViIjoiZ286
MTAyOTA1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6IndoYXQgaX
MgdGhlIGVxdWF0aW9uPyBTaW5jZSBJIGRvbid0IGtub3csIHBl
cmhhcHMgeW91IGNhbiBiZSBtb3JlIHNwZWNpZmljIiwiY3JlYX
RlZCI6MTU0NDU1ODcwMzg4Mn0sIlp0OXJHV0hvSnVzdTV3S3Yi
OnsiZGlzY3Vzc2lvbklkIjoiWFoydTdicmVNNU5CZlM2UiIsIn
N1YiI6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQi
OiJXaGF0IGtpbmQgb2Ygb2JqZWN0cz8gQXJlIHRoZXkgY2FsbG
VkIG51bWVyaWNhbCBhcnJheXMgb3Igc29tZXRoaW5nPyIsImNy
ZWF0ZWQiOjE1NDQ1NTg3OTMzOTB9LCJFMzIxVndsbENHODhlR0
pnIjp7ImRpc2N1c3Npb25JZCI6IkhodWlweTNoZk9qZ25vRFMi
LCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZX
h0IjoiQSBnZW5lcmFsIGNvbW1lbnQgb24gaHlwZXJsaW5rcy4g
SSBrbm93IHRoaXMgam91cm5hbCBpcyB2ZXJ5IGRpZ2l0YWxseS
BvcmllbnRlZCwgYnV0IEkndmUgc3RhcnRlZCB1c2luZyB0aGUg
Zm9sbG93aW5nIHBhcmFkaWdtIGZvciBpbXBvcnRhbnQgaHlwZX
JsaW5rczogZm9yIHRoZSBkaXNwbGF5ZWQgdGV4dCwgSSB1c2Ug
dGhlIGZ1bGwgVVJMIChleGNlcHQgdGhlIFwiaHR0cHM6Ly93d3
cuXCIpLCBvbiBpdHMgb3duIGxpbmUsIGNlbnRlcmVkLCBpbiB0
eXBld3JpdGVyIGZvbnQsIHdpdGhvdXQgYSBzZWxlY3RhYmxlIH
BlcmlvZCBhdCB0aGUgZW5kIChpbiBMYVRlWCBJIGNhbiBtYWtl
IGFuIHVuc2VsZWN0YWJsZSBwZXJpb2QpLiBJJ20gbm90IHN1cm
UgaWYgeW91IHdhbnQgdG8gYWRvcHQgc29tZXRoaW5nIHNpbWls
YXIsIGhlcmUsIGJ1dCBpdCBoYXMgdGhlIGFkdmFudGFnZSBvZi
BzdXJ2aXZpbmcgcHJpbnRpbmcgYW5kIGNhbGxpbmcgYXR0ZW50
aW9uIHRvIHRoZSBVUkwiLCJjcmVhdGVkIjoxNTQ0NTU5MDcxOD
MwfX0sImhpc3RvcnkiOlstMTM0OTE1NjcwNSwxMTMzMjQ0NjY0
LC0xMjYwNTU0NTUwLC0xNjgzNDY5NDQ5LC0xMTcxNTA5Nzk5LC
0yNjc3NjYzOTUsLTU1Njk0MDMwNyw0MzM3NDQ2OTMsLTM4NzUz
MjkyMCwzMjMzMjY2ODQsNTEyNjA5NTk2LC0xOTQ5NDEzNjAyLC
00MjIwNDE1OTUsLTE2NTU1Njg0MTQsLTEyMDk3NTA3OTYsLTcz
NTYwNTQ2NSwxNzE3MjAwMDg2LC0xNTEzOTA1MDA3LDIwMjIyOT
UzNzcsLTkyMDk2OTY2M119
-->