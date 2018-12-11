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
This function returns an object which includes the resulting system as a state-space model, a transfer function, and a state equation.
Auxiliary functions are included to convert the SymPy symbolic matrices to Numpy [@oliphant2015] objects.
This package is documented at [statemint.readthedocs.io](https://statemint.readthedocs.io/en/latest/) and works for both linear and nonlinear systems.

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
wic3RhcnQiOjQ0ODAsImVuZCI6NDQ5MX0sIlhaMnU3YnJlTTVO
QmZTNlIiOnsidGV4dCI6Im9iamVjdHMiLCJzdGFydCI6NDYzOS
wiZW5kIjo0NjQ2fX0sImNvbW1lbnRzIjp7IkV1T1V2YkZpSDVx
VG5LUTAiOnsiZGlzY3Vzc2lvbklkIjoidkFpQTFLZ0FCbWtZT2
NNZSIsInN1YiI6ImdoOjEwMzk0ODk2IiwidGV4dCI6IlNob3Vs
ZCB3ZSBjaXRlIEJBU0lDIG5vdGF0aW9uPyBJIGZvdW5kIGl0IG
9uIFdpa2lwZWRpYSwgIFxuW2h0dHBzOi8vZW4ud2lraXBlZGlh
Lm9yZy93aWtpL0NhbGN1bGF0b3JfaW5wdXRfbWV0aG9kcyNCQV
NJQ19ub3RhdGlvbl0oaHR0cHM6Ly9lbi53aWtpcGVkaWEub3Jn
L3dpa2kvQ2FsY3VsYXRvcl9pbnB1dF9tZXRob2RzI0JBU0lDX2
5vdGF0aW9uKSIsImNyZWF0ZWQiOjE1NDM5NTM3NTQ2NDl9LCJF
VUQ2WkVZS3NPWllBV3FmIjp7ImRpc2N1c3Npb25JZCI6InZBaU
ExS2dBQm1rWU9jTWUiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4
OTY0NzQ4MDAiLCJ0ZXh0IjoiSSB0aGluayB0aGF0IHdvdWxkIG
JlIGdvb2QgdG8gY2l0ZSBpdCAuLi4gQkFTSUMgaXMgYSBsYW5n
dWFnZSwgcmlnaHQ/IFNvIEknZCBjaXRlIGl0IGhvd2V2ZXIgeW
91J3ZlIGJlZW4gY2l0aW5nIHRoZSBvdGhlcnMgLi4uIiwiY3Jl
YXRlZCI6MTU0NDUxNjI2MTM3NX0sImhaQktPWXlnOFFtVE1Pcn
EiOnsiZGlzY3Vzc2lvbklkIjoidHRuaGhacXY4anpEanprZSIs
InN1YiI6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleH
QiOiJEaWQgSSBwcm9wZXJseSBjbGFyaWZ5IHRoaXM/IiwiY3Jl
YXRlZCI6MTU0NDU1NzMyOTc0Mn0sImFKZTZHQlk1bGlRY25JWW
YiOnsiZGlzY3Vzc2lvbklkIjoidHRuaGhacXY4anpEanprZSIs
InN1YiI6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleH
QiOiJBbHNvLCBkb2VzIGl0IGFsbG93IHNvbWVvbmUgdG8gaG9v
ayB1cCB0aGVpciBvd24gQVdTIGluc3RhbmNlIC4uLiBhbmQgZG
lkIHlvdSBpbmNsdWRlIGRvY3Mgb24gaG93IHRvIGdldCB0aGUg
QVdTIHNldCB1cD8iLCJjcmVhdGVkIjoxNTQ0NTU3Mzg3OTI4fS
wiaWwxdE9qUzc1MU45UVdoViI6eyJkaXNjdXNzaW9uSWQiOiJH
N0p4aFpKR2VVelJvaEhPIiwic3ViIjoiZ286MTAyOTA1NDM1NT
MwODk2NDc0ODAwIiwidGV4dCI6IldlIHNob3VsZCBkb3VibGUg
Y2hlY2sgdGhhdCB3ZSdyZSBjb25zaXN0ZW50bHkgaHlwaGVuYX
Rpbmcgc3RhdGUtc3BhY2UgLi4uIGl0J3MgdGhlIHN0YW5kYXJk
IHVzYWdlIiwiY3JlYXRlZCI6MTU0NDU1ODY2Nzg5N30sIlp0OX
JHV0hvSnVzdTV3S3YiOnsiZGlzY3Vzc2lvbklkIjoiWFoydTdi
cmVNNU5CZlM2UiIsInN1YiI6ImdvOjEwMjkwNTQzNTUzMDg5Nj
Q3NDgwMCIsInRleHQiOiJXaGF0IGtpbmQgb2Ygb2JqZWN0cz8g
QXJlIHRoZXkgY2FsbGVkIG51bWVyaWNhbCBhcnJheXMgb3Igc2
9tZXRoaW5nPyIsImNyZWF0ZWQiOjE1NDQ1NTg3OTMzOTB9LCJW
N0pyTmtQc3pqTEZWdFAyIjp7ImRpc2N1c3Npb25JZCI6InR0bm
hoWnF2OGp6RGp6a2UiLCJzdWIiOiJnaDoxMDM5NDg5NiIsInRl
eHQiOiJUaGUgaW5zdGFsbGVyIGRlcGxveXMgdGhlIG5lY2Vzc2
FyeSBjb2RlIHRvIHRoZWlyIEFXUyBhY2NvdW50LCB0aGVuIHBs
YWNlcyB0aGUgbmVjZXNzYXJ5IGZpbGVzIGluIHRoZSBgd2ViL0
hUTUxgIGZvbGRlciBzbyB0aG9zZSBmaWxlcyBjYW4gYmUgdXBs
b2FkZWQgdG8gYSB3ZWIgc2VydmVyLiIsImNyZWF0ZWQiOjE1ND
Q1NjAxNTE4NDh9fSwiaGlzdG9yeSI6Wy0yMDQ1MjMzMzE4LDEx
MzMyNDQ2NjQsLTEyNjA1NTQ1NTAsLTE2ODM0Njk0NDksLTExNz
E1MDk3OTksLTI2Nzc2NjM5NSwtNTU2OTQwMzA3LDQzMzc0NDY5
MywtMzg3NTMyOTIwLDMyMzMyNjY4NCw1MTI2MDk1OTYsLTE5ND
k0MTM2MDIsLTQyMjA0MTU5NSwtMTY1NTU2ODQxNCwtMTIwOTc1
MDc5NiwtNzM1NjA1NDY1LDE3MTcyMDAwODYsLTE1MTM5MDUwMD
csMjAyMjI5NTM3NywtOTIwOTY5NjYzXX0=
-->