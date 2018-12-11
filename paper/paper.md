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
bmQiOjI4Nzl9LCJsdmNEODBUSHYyUTlLTVQ3Ijp7InN0YXJ0Ij
ozMzg3LCJlbmQiOjMzOTUsInRleHQiOiJ0dXRvcmlhbCJ9LCJ0
dG5oaFpxdjhqekRqemtlIjp7InN0YXJ0IjozOTg1LCJlbmQiOj
QxNTcsInRleHQiOiJBbiBhdXRvbWF0ZWQgaW5zdGFsbGVyIGZv
ciBpbmRlcGVuZGVudCBkZXBsb3ltZW50IG9mIHRoZSB3ZWJzaX
RlIGlzIGFsc28gW2luY2x14oCmIn0sIkc3SnhoWkpHZVV6Um9o
SE8iOnsic3RhcnQiOjQ0MTAsImVuZCI6NDQyMSwidGV4dCI6In
N0YXRlLXNwYWNlIn0sInBMcVpXV0wydXdQVkhXekMiOnsic3Rh
cnQiOjQ0NTQsImVuZCI6NDQ2NSwidGV4dCI6ImFuIGVxdWF0aW
9uIn0sIlhaMnU3YnJlTTVOQmZTNlIiOnsic3RhcnQiOjQ1NjQs
ImVuZCI6NDU3MSwidGV4dCI6Im9iamVjdHMifSwiSGh1aXB5M2
hmT2pnbm9EUyI6eyJzdGFydCI6NDU3MywiZW5kIjo0NzEzLCJ0
ZXh0IjoiVGhpcyBjb2RlIGlzIGRvY3VtZW50ZWQgYXQgW3JlYW
R0aGVkb2NzLmlvXShodHRwczovL3N0YXRlbWludC5yZWFkdGhl
ZG9jcy5pby9lbuKApiJ9fSwiY29tbWVudHMiOnsiRXVPVXZiRm
lINXFUbktRMCI6eyJkaXNjdXNzaW9uSWQiOiJ2QWlBMUtnQUJt
a1lPY01lIiwic3ViIjoiZ2g6MTAzOTQ4OTYiLCJ0ZXh0IjoiU2
hvdWxkIHdlIGNpdGUgQkFTSUMgbm90YXRpb24/IEkgZm91bmQg
aXQgb24gV2lraXBlZGlhLCAgXG5baHR0cHM6Ly9lbi53aWtpcG
VkaWEub3JnL3dpa2kvQ2FsY3VsYXRvcl9pbnB1dF9tZXRob2Rz
I0JBU0lDX25vdGF0aW9uXShodHRwczovL2VuLndpa2lwZWRpYS
5vcmcvd2lraS9DYWxjdWxhdG9yX2lucHV0X21ldGhvZHMjQkFT
SUNfbm90YXRpb24pIiwiY3JlYXRlZCI6MTU0Mzk1Mzc1NDY0OX
0sIkVVRDZaRVlLc09aWUFXcWYiOnsiZGlzY3Vzc2lvbklkIjoi
dkFpQTFLZ0FCbWtZT2NNZSIsInN1YiI6ImdvOjEwMjkwNTQzNT
UzMDg5NjQ3NDgwMCIsInRleHQiOiJJIHRoaW5rIHRoYXQgd291
bGQgYmUgZ29vZCB0byBjaXRlIGl0IC4uLiBCQVNJQyBpcyBhIG
xhbmd1YWdlLCByaWdodD8gU28gSSdkIGNpdGUgaXQgaG93ZXZl
ciB5b3UndmUgYmVlbiBjaXRpbmcgdGhlIG90aGVycyAuLi4iLC
JjcmVhdGVkIjoxNTQ0NTE2MjYxMzc1fSwiSko1d1BPS1FXeFRL
MFBVdSI6eyJkaXNjdXNzaW9uSWQiOiJsdmNEODBUSHYyUTlLTV
Q3Iiwic3ViIjoiZ286MTAyOTA1NDM1NTMwODk2NDc0ODAwIiwi
dGV4dCI6ImhyZWYiLCJjcmVhdGVkIjoxNTQ0NTU3MjkzMjI4fS
wiaFpCS09ZeWc4UW1UTU9ycSI6eyJkaXNjdXNzaW9uSWQiOiJ0
dG5oaFpxdjhqekRqemtlIiwic3ViIjoiZ286MTAyOTA1NDM1NT
MwODk2NDc0ODAwIiwidGV4dCI6IkRpZCBJIHByb3Blcmx5IGNs
YXJpZnkgdGhpcz8iLCJjcmVhdGVkIjoxNTQ0NTU3MzI5NzQyfS
wiYUplNkdCWTVsaVFjbklZZiI6eyJkaXNjdXNzaW9uSWQiOiJ0
dG5oaFpxdjhqekRqemtlIiwic3ViIjoiZ286MTAyOTA1NDM1NT
MwODk2NDc0ODAwIiwidGV4dCI6IkFsc28sIGRvZXMgaXQgYWxs
b3cgc29tZW9uZSB0byBob29rIHVwIHRoZWlyIG93biBBV1MgaW
5zdGFuY2UgLi4uIGFuZCBkaWQgeW91IGluY2x1ZGUgZG9jcyBv
biBob3cgdG8gZ2V0IHRoZSBBV1Mgc2V0IHVwPyIsImNyZWF0ZW
QiOjE1NDQ1NTczODc5Mjh9LCJpbDF0T2pTNzUxTjlRV2hWIjp7
ImRpc2N1c3Npb25JZCI6Ikc3SnhoWkpHZVV6Um9oSE8iLCJzdW
IiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZXh0Ijoi
V2Ugc2hvdWxkIGRvdWJsZSBjaGVjayB0aGF0IHdlJ3JlIGNvbn
Npc3RlbnRseSBoeXBoZW5hdGluZyBzdGF0ZS1zcGFjZSAuLi4g
aXQncyB0aGUgc3RhbmRhcmQgdXNhZ2UiLCJjcmVhdGVkIjoxNT
Q0NTU4NjY3ODk3fSwiZEtiUUc4MkRSQ3k0RkZkNCI6eyJkaXNj
dXNzaW9uSWQiOiJwTHFaV1dMMnV3UFZIV3pDIiwic3ViIjoiZ2
86MTAyOTA1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6IndoYXQg
aXMgdGhlIGVxdWF0aW9uPyBTaW5jZSBJIGRvbid0IGtub3csIH
BlcmhhcHMgeW91IGNhbiBiZSBtb3JlIHNwZWNpZmljIiwiY3Jl
YXRlZCI6MTU0NDU1ODcwMzg4Mn0sIlp0OXJHV0hvSnVzdTV3S3
YiOnsiZGlzY3Vzc2lvbklkIjoiWFoydTdicmVNNU5CZlM2UiIs
InN1YiI6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleH
QiOiJXaGF0IGtpbmQgb2Ygb2JqZWN0cz8gQXJlIHRoZXkgY2Fs
bGVkIG51bWVyaWNhbCBhcnJheXMgb3Igc29tZXRoaW5nPyIsIm
NyZWF0ZWQiOjE1NDQ1NTg3OTMzOTB9LCJFMzIxVndsbENHODhl
R0pnIjp7ImRpc2N1c3Npb25JZCI6IkhodWlweTNoZk9qZ25vRF
MiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0
ZXh0IjoiQSBnZW5lcmFsIGNvbW1lbnQgb24gaHlwZXJsaW5rcy
4gSSBrbm93IHRoaXMgam91cm5hbCBpcyB2ZXJ5IGRpZ2l0YWxs
eSBvcmllbnRlZCwgYnV0IEkndmUgc3RhcnRlZCB1c2luZyB0aG
UgZm9sbG93aW5nIHBhcmFkaWdtIGZvciBpbXBvcnRhbnQgaHlw
ZXJsaW5rczogZm9yIHRoZSBkaXNwbGF5ZWQgdGV4dCwgSSB1c2
UgdGhlIGZ1bGwgVVJMIChleGNlcHQgdGhlIFwiaHR0cHM6Ly93
d3cuXCIpLCBvbiBpdHMgb3duIGxpbmUsIGNlbnRlcmVkLCBpbi
B0eXBld3JpdGVyIGZvbnQsIHdpdGhvdXQgYSBzZWxlY3RhYmxl
IHBlcmlvZCBhdCB0aGUgZW5kIChpbiBMYVRlWCBJIGNhbiBtYW
tlIGFuIHVuc2VsZWN0YWJsZSBwZXJpb2QpLiBJJ20gbm90IHN1
cmUgaWYgeW91IHdhbnQgdG8gYWRvcHQgc29tZXRoaW5nIHNpbW
lsYXIsIGhlcmUsIGJ1dCBpdCBoYXMgdGhlIGFkdmFudGFnZSBv
ZiBzdXJ2aXZpbmcgcHJpbnRpbmcgYW5kIGNhbGxpbmcgYXR0ZW
50aW9uIHRvIHRoZSBVUkwiLCJjcmVhdGVkIjoxNTQ0NTU5MDcx
ODMwfX0sImhpc3RvcnkiOlsxMTMzMjQ0NjY0LC0xMjYwNTU0NT
UwLC0xNjgzNDY5NDQ5LC0xMTcxNTA5Nzk5LC0yNjc3NjYzOTUs
LTU1Njk0MDMwNyw0MzM3NDQ2OTMsLTM4NzUzMjkyMCwzMjMzMj
Y2ODQsNTEyNjA5NTk2LC0xOTQ5NDEzNjAyLC00MjIwNDE1OTUs
LTE2NTU1Njg0MTQsLTEyMDk3NTA3OTYsLTczNTYwNTQ2NSwxNz
E3MjAwMDg2LC0xNTEzOTA1MDA3LDIwMjIyOTUzNzcsLTkyMDk2
OTY2Myw4NzQ0MDIxOTFdfQ==
-->