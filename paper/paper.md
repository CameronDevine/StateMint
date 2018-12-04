---
title: 'StateMint: An Application for Determining Symbolic Dynamic System Models using Linear Graph Methods'
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



# Summary

When determining the differential equation of a dynamic system using linear graph methods finding the elemental and constraint equations is the first step.
The next step is to algebraically eliminate those variables that are not state or input variables from the equations until a minimal set of differential equations remains.
During this step of manually reducing the system of equations is where students often make mistakes, leading to frustration and discouragement.
However, this algebra is not a necessary component of a strong understanding of system dynamics and can be easily automated using tools we present here.
These tools 

To aid students in their learning process a program was written to symbolically determine the differential equations using the elemental and constraint equations as input.
This program allows students to focus on the process of creating a dynamic system model without worrying about algebraic mistakes.
This allows the student to focus on course content which is new and unique.

Utilizing the advanced symbolic mathematics capabilities of Mathematica, a package was written to determine the differential equation.
However, this requires students to purchase, install, and learn Mathematica, often with a considerable monetary investment and learning curve.
To mitigate these problems a web app was designed to allow students to use this tool without any knowledge of programming by allowing equations to be input in BASIC notation, similar to most scientific calculators.
To support this interface a Python package was written with the same functionality as the Mathematica package and run as an Amazon AWS Lambda function.
With the Lambda function running in the cloud this software can be used by any device with an internet connection and web browser.

# Web Interface

To allow those without programming experience to use this code a web interface was designed and [implemented](http://statum.camerondevine.me/).
This interface has text boxes for equation input, and displays results as rendered math or code which can be copied into \LaTeX, Matlab, Python, or Mathematica.
Examples and documentation are built in to make learning how to use the interface as painless as possible.
There is also the ability to share, download, and save the system models for later use or modification.
This interface is designed to run on Amazon AWS serverless resources to simplify upkeep and keep costs low.
An automated installer is also [included](https://github.com/CameronDevine/Statum/tree/master/web).

# Python Package

The Python package for performing the same task uses similar logic to the second method of the Mathematica package, again in the form defined by Rowell and Wormley [@rowell1997].
This function returns an object which includes the resulting system as a state space model, a transfer function, and an equation.
Helper functions are included to convert the symbolic matrices to Numpy [@oliphant2015] objects.
This code is documented using [readthedocs.io](https://statum.readthedocs.io/en/latest/) and works for both linear and nonlinear systems.

The excellent Python symbolic mathematics library, SymPy [@meurer2017], was instrumental in this implementation.

# Mathematica Package

The Mathematica package `StateMint` can be installed via the [documentation](https://github.com/CameronDevine/Statum/blob/master/mathematica/README.md). The central function of the package is `stateEquations`, which uses an algorithm similar to that of the Python package, above, to derive the state equations. It takes as arguments lists of elemental equations, constraint equations, primary variables, and input variables and returns the vector state equation, state variables, and the time-derivative of the state variables.

The `outputEquations` function derives the output equations given output expressions in terms of primary and secondary variables (including inputs). The function accepts lists of input variables, state variables, elemental and constraint equations, and output expressions.

The functions `stateEquations` and `outputEquations` yield what are in general *nonlinear* state and output equations. Linear state and output equations are typically written in a standard vector form described by matrices `A`, `B`, `C`, and `D` (and sometimes `E` and `F`). The `linearizeState` function accepts lists of input variables, state variables, and the time-derivatives of the state vector (from `stateEquations`) and returns the `A`, `B`, and `E` matrices. Similarly, `linearizeOutput` returns the `C`, `D`, and `F` matrices.

An example of how to use this package is [included](https://github.com/CameronDevine/Statum/blob/master/mathematica/Example.nb).

# Acknowledgments

The authors would like to acknowledge the work of [Gavin Basuel](https://www.gavinbasuel.com/) who designed the user experience for the web interface and helped with HTML/CSS development.

# References

<!--stackedit_data:
eyJkaXNjdXNzaW9ucyI6eyJTUjhYckl2em11VWpGY1paIjp7In
N0YXJ0Ijo2NzksImVuZCI6ODM0LCJ0ZXh0IjoiV2hlbiBkZXRl
cm1pbmluZyB0aGUgZGlmZmVyZW50aWFsIGVxdWF0aW9uIG9mIG
EgZHluYW1pYyBzeXN0ZW0gdXNpbmcgbGluZWFyIGdyYeKApiJ9
LCJrSXRMMVFWQkhJeWttVEJ0Ijp7InN0YXJ0IjoxMzE4LCJlbm
QiOjE0ODksInRleHQiOiJUbyBhaWQgc3R1ZGVudHMgaW4gdGhl
aXIgbGVhcm5pbmcgcHJvY2VzcyBhIHByb2dyYW0gd2FzIHdyaX
R0ZW4gdG8gc3ltYm9saWNhbGx54oCmIn0sInZBaUExS2dBQm1r
WU9jTWUiOnsic3RhcnQiOjIxMzUsImVuZCI6MjE0OSwidGV4dC
I6IkJBU0lDIG5vdGF0aW9uIn19LCJjb21tZW50cyI6eyJSeUxq
azJxTGNyOERzOEpkIjp7ImRpc2N1c3Npb25JZCI6IlNSOFhySX
Z6bXVVakZjWloiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0
NzQ4MDAiLCJ0ZXh0IjoiSSdtIGEgYmlnIGJlbGlldmVyIHRoYX
QgeW91ciBmaXJzdCBzZW50ZW5jZSBzaG91bGQgdHJ5IHRvIGNv
bnZleSB0aGUgbWFpbiBwb2ludCBvZiB5b3VyIHBhcGVyLiBUaG
lzIGlzIG1vcmUgb2YgYW4gXCJpbnRyb2R1Y3Rpb25cIiBzZWN0
aW9uIHNlbnRlbmNlLCBhcyBhcmUgdGhvc2UgdGhhdCBmb2xsb3
cgaXQuIFBlcmhhcHMgdGhpcyAqaXMqIGVmZmVjdGl2ZWx5IHRo
ZSBpbnRyb2R1Y3Rpb24gYW5kIHRoZXJlJ3MgYSBzZXBhcmF0ZS
BhYnN0cmFjdCAuLi4gaWYgc28sIHRoYXQncyBmaW5lLiIsImNy
ZWF0ZWQiOjE1NDM3MTkxMDI4MzB9LCJ6ZGh3Y01aaWVEV3JJcG
tDIjp7ImRpc2N1c3Npb25JZCI6IlNSOFhySXZ6bXVVakZjWloi
LCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZX
h0IjoiSSdtIGdvaW5nIHRvIGNvbnRpbnVlIGNvbW1lbnRpbmcg
YXMgaWYgdGhpcyB0ZXh0IGlzIHByZWNlZGVkIGJ5IGFuIGFic3
RyYWN0IG9mIHNvbWUgc29ydC4iLCJjcmVhdGVkIjoxNTQzNzE5
MjAxODA4fSwiNEJyY05qc0RseFNiTGxNNiI6eyJkaXNjdXNzaW
9uSWQiOiJrSXRMMVFWQkhJeWttVEJ0Iiwic3ViIjoiZ286MTAy
OTA1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6IldlIGNhbiBub3
cgYmUgbW9yZSBzcGVjaWZpYywgaGVyZS4gV2UgaGF2ZSBhbHJl
YWR5IGludHJvZHVjZWQgdGhlIGVxdWF0aW9ucyBhbmQgdGhlIH
Rhc2sgb2YgYXV0b21hdGlvbi4iLCJjcmVhdGVkIjoxNTQzNzIw
MDYzNjkyfSwiRXVPVXZiRmlINXFUbktRMCI6eyJkaXNjdXNzaW
9uSWQiOiJ2QWlBMUtnQUJta1lPY01lIiwic3ViIjoiZ2g6MTAz
OTQ4OTYiLCJ0ZXh0IjoiU2hvdWxkIHdlIGNpdGUgQkFTSUMgbm
90YXRpb24/IEkgZm91bmQgaXQgb24gV2lraXBlZGlhLCAgXG5b
aHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvQ2FsY3VsYX
Rvcl9pbnB1dF9tZXRob2RzI0JBU0lDX25vdGF0aW9uXShodHRw
czovL2VuLndpa2lwZWRpYS5vcmcvd2lraS9DYWxjdWxhdG9yX2
lucHV0X21ldGhvZHMjQkFTSUNfbm90YXRpb24pIiwiY3JlYXRl
ZCI6MTU0Mzk1Mzc1NDY0OX19LCJoaXN0b3J5IjpbNjE4OTk3OT
I5LC0xNzYyMDM3Mzg4LC01NzUzNDM3MTAsNjcwNDQ3NzEsLTIy
OTEzNTc2OSwtMTEyMzM5MjA1NCwtODg3MzAxODIsMjEwMTkyND
Y4NSw2MDIwNzk3ODAsMTA4NTMwNzM4MiwtMTQ1MTc3OTQyMywt
MTAwOTk1ODAyNyw0ODQyNDgyMTgsMTEzMjIyMzg5MywtNTYwMz
g3MjU1LC0zMzI2MjE3MDYsMTY4MjUzMDQ5MywtMTQ5MjkwOTU3
LDQyMzY2MDExLC0yNTY5NjU4MzddfQ==
-->