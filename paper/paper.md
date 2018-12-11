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
wiZW5kIjo0NjQ2fSwiSGh1aXB5M2hmT2pnbm9EUyI6eyJ0ZXh0
IjoiVGhpcyBjb2RlIGlzIGRvY3VtZW50ZWQgYXQgW3JlYWR0aG
Vkb2NzLmlvXShodHRwczovL3N0YXRlbWludC5yZWFkdGhlZG9j
cy5pby9lbuKApiIsInN0YXJ0Ijo0NjQ4LCJlbmQiOjQ3OTh9fS
wiY29tbWVudHMiOnsiRXVPVXZiRmlINXFUbktRMCI6eyJkaXNj
dXNzaW9uSWQiOiJ2QWlBMUtnQUJta1lPY01lIiwic3ViIjoiZ2
g6MTAzOTQ4OTYiLCJ0ZXh0IjoiU2hvdWxkIHdlIGNpdGUgQkFT
SUMgbm90YXRpb24/IEkgZm91bmQgaXQgb24gV2lraXBlZGlhLC
AgXG5baHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvQ2Fs
Y3VsYXRvcl9pbnB1dF9tZXRob2RzI0JBU0lDX25vdGF0aW9uXS
hodHRwczovL2VuLndpa2lwZWRpYS5vcmcvd2lraS9DYWxjdWxh
dG9yX2lucHV0X21ldGhvZHMjQkFTSUNfbm90YXRpb24pIiwiY3
JlYXRlZCI6MTU0Mzk1Mzc1NDY0OX0sIkVVRDZaRVlLc09aWUFX
cWYiOnsiZGlzY3Vzc2lvbklkIjoidkFpQTFLZ0FCbWtZT2NNZS
IsInN1YiI6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRl
eHQiOiJJIHRoaW5rIHRoYXQgd291bGQgYmUgZ29vZCB0byBjaX
RlIGl0IC4uLiBCQVNJQyBpcyBhIGxhbmd1YWdlLCByaWdodD8g
U28gSSdkIGNpdGUgaXQgaG93ZXZlciB5b3UndmUgYmVlbiBjaX
RpbmcgdGhlIG90aGVycyAuLi4iLCJjcmVhdGVkIjoxNTQ0NTE2
MjYxMzc1fSwiaFpCS09ZeWc4UW1UTU9ycSI6eyJkaXNjdXNzaW
9uSWQiOiJ0dG5oaFpxdjhqekRqemtlIiwic3ViIjoiZ286MTAy
OTA1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6IkRpZCBJIHByb3
Blcmx5IGNsYXJpZnkgdGhpcz8iLCJjcmVhdGVkIjoxNTQ0NTU3
MzI5NzQyfSwiYUplNkdCWTVsaVFjbklZZiI6eyJkaXNjdXNzaW
9uSWQiOiJ0dG5oaFpxdjhqekRqemtlIiwic3ViIjoiZ286MTAy
OTA1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6IkFsc28sIGRvZX
MgaXQgYWxsb3cgc29tZW9uZSB0byBob29rIHVwIHRoZWlyIG93
biBBV1MgaW5zdGFuY2UgLi4uIGFuZCBkaWQgeW91IGluY2x1ZG
UgZG9jcyBvbiBob3cgdG8gZ2V0IHRoZSBBV1Mgc2V0IHVwPyIs
ImNyZWF0ZWQiOjE1NDQ1NTczODc5Mjh9LCJpbDF0T2pTNzUxTj
lRV2hWIjp7ImRpc2N1c3Npb25JZCI6Ikc3SnhoWkpHZVV6Um9o
SE8iLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLC
J0ZXh0IjoiV2Ugc2hvdWxkIGRvdWJsZSBjaGVjayB0aGF0IHdl
J3JlIGNvbnNpc3RlbnRseSBoeXBoZW5hdGluZyBzdGF0ZS1zcG
FjZSAuLi4gaXQncyB0aGUgc3RhbmRhcmQgdXNhZ2UiLCJjcmVh
dGVkIjoxNTQ0NTU4NjY3ODk3fSwiWnQ5ckdXSG9KdXN1NXdLdi
I6eyJkaXNjdXNzaW9uSWQiOiJYWjJ1N2JyZU01TkJmUzZSIiwi
c3ViIjoiZ286MTAyOTA1NDM1NTMwODk2NDc0ODAwIiwidGV4dC
I6IldoYXQga2luZCBvZiBvYmplY3RzPyBBcmUgdGhleSBjYWxs
ZWQgbnVtZXJpY2FsIGFycmF5cyBvciBzb21ldGhpbmc/IiwiY3
JlYXRlZCI6MTU0NDU1ODc5MzM5MH0sIkUzMjFWd2xsQ0c4OGVH
SmciOnsiZGlzY3Vzc2lvbklkIjoiSGh1aXB5M2hmT2pnbm9EUy
IsInN1YiI6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRl
eHQiOiJBIGdlbmVyYWwgY29tbWVudCBvbiBoeXBlcmxpbmtzLi
BJIGtub3cgdGhpcyBqb3VybmFsIGlzIHZlcnkgZGlnaXRhbGx5
IG9yaWVudGVkLCBidXQgSSd2ZSBzdGFydGVkIHVzaW5nIHRoZS
Bmb2xsb3dpbmcgcGFyYWRpZ20gZm9yIGltcG9ydGFudCBoeXBl
cmxpbmtzOiBmb3IgdGhlIGRpc3BsYXllZCB0ZXh0LCBJIHVzZS
B0aGUgZnVsbCBVUkwgKGV4Y2VwdCB0aGUgXCJodHRwczovL3d3
dy5cIiksIG9uIGl0cyBvd24gbGluZSwgY2VudGVyZWQsIGluIH
R5cGV3cml0ZXIgZm9udCwgd2l0aG91dCBhIHNlbGVjdGFibGUg
cGVyaW9kIGF0IHRoZSBlbmQgKGluIExhVGVYIEkgY2FuIG1ha2
UgYW4gdW5zZWxlY3RhYmxlIHBlcmlvZCkuIEknbSBub3Qgc3Vy
ZSBpZiB5b3Ugd2FudCB0byBhZG9wdCBzb21ldGhpbmcgc2ltaW
xhciwgaGVyZSwgYnV0IGl0IGhhcyB0aGUgYWR2YW50YWdlIG9m
IHN1cnZpdmluZyBwcmludGluZyBhbmQgY2FsbGluZyBhdHRlbn
Rpb24gdG8gdGhlIFVSTCIsImNyZWF0ZWQiOjE1NDQ1NTkwNzE4
MzB9LCJWN0pyTmtQc3pqTEZWdFAyIjp7ImRpc2N1c3Npb25JZC
I6InR0bmhoWnF2OGp6RGp6a2UiLCJzdWIiOiJnaDoxMDM5NDg5
NiIsInRleHQiOiJUaGUgaW5zdGFsbGVyIGRlcGxveXMgdGhlIG
5lY2Vzc2FyeSBjb2RlIHRvIHRoZWlyIEFXUyBhY2NvdW50LCB0
aGVuIHBsYWNlcyB0aGUgbmVjZXNzYXJ5IGZpbGVzIGluIHRoZS
Bgd2ViL0hUTUxgIGZvbGRlciBzbyB0aG9zZSBmaWxlcyBjYW4g
YmUgdXBsb2FkZWQgdG8gYSB3ZWIgc2VydmVyLiIsImNyZWF0ZW
QiOjE1NDQ1NjAxNTE4NDh9fSwiaGlzdG9yeSI6Wy0xMDY5ODA5
ODU3LDExMzMyNDQ2NjQsLTEyNjA1NTQ1NTAsLTE2ODM0Njk0ND
ksLTExNzE1MDk3OTksLTI2Nzc2NjM5NSwtNTU2OTQwMzA3LDQz
Mzc0NDY5MywtMzg3NTMyOTIwLDMyMzMyNjY4NCw1MTI2MDk1OT
YsLTE5NDk0MTM2MDIsLTQyMjA0MTU5NSwtMTY1NTU2ODQxNCwt
MTIwOTc1MDc5NiwtNzM1NjA1NDY1LDE3MTcyMDAwODYsLTE1MT
M5MDUwMDcsMjAyMjI5NTM3NywtOTIwOTY5NjYzXX0=
-->