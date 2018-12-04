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

StateMint is a set of tools which solve sets of equations to find dynamic system models.
When derived by hand there is a considerable chance of 

# Introduction

When determining the differential equation of a dynamic system using linear graph methods finding the elemental and constraint equations is the first step.
The next step is to algebraically eliminate those variables that are not state or input variables from the equations until a minimal set of differential equations remains.
During this step of manually reducing the system of equations is where students often make mistakes, leading to frustration and discouragement.
However, this algebra is not a necessary component of a strong understanding of system dynamics and can be easily automated using tools we present here.
These tools allow students to focus on the process of creating a dynamic system model without worrying about algebraic mistakes.
This allows the student to focus on course content which is new and unique.

Utilizing the advanced symbolic mathematics capabilities of Mathematica, a package was written to determine the dynamic system model.
However, this requires students to purchase, install, and learn Mathematica, often with a considerable monetary investment and learning curve.
To mitigate these problems a web app was designed to allow students to use this tool without any knowledge of programming by allowing equations to be input in BASIC notation, similar to most scientific calculators.
To support this interface a Python package was written with the same functionality as the Mathematica package and run as an Amazon AWS Lambda function.
With the Lambda function running in the cloud this software can be used by any device with an internet connection and a web browser.

# Web Interface

The [web interface](http://statum.camerondevine.me/) has text boxes for equations to be input.
These equations must be entered in the form defined by Rowell and Wormley [@rowell1997].
Once entered, the equations are sent to the Lambda function and the dynamic system model is returned.
The results are then displayed as rendered math or code which can be copied into \LaTeX, Matlab, Python, or Mathematica.
Examples and documentation are built in to make learning how to use the interface as painless as possible.
There is also the ability to share, download, and save the dynamic system models for later use or modification.
Because this interface utilizes Amazon AWS serverless resources, required maintenance and costs are minimized.
An automated installer is also [included](https://github.com/CameronDevine/Statum/tree/master/web).

# Python Package

The Python package uses the SymPy [@meurer2017] library to symbolically eliminate the unneeded variables.
This function returns an object which includes the resulting system as a state space model, a transfer function, and an equation.
Helper functions are included to convert the symbolic matrices to Numpy [@oliphant2015] objects.
This code is documented using [readthedocs.io](https://statum.readthedocs.io/en/latest/) and works for both linear and nonlinear systems.

An example of how to use this package is [included](https://github.com/CameronDevine/Statum/blob/master/python/Example.ipynb).

# Mathematica Package

The Mathematica package `StateMint` can be installed as described in the [documentation](https://github.com/CameronDevine/Statum/blob/master/mathematica/README.md). The central function of the package is `stateEquations`, which uses an algorithm similar to that of the Python package, above, to derive the state equations. It takes as arguments lists of elemental equations, constraint equations, primary variables, and input variables and returns the vector state equation, state variables, and the time-derivative of the state variables.

The `outputEquations` function derives the output equations given output expressions in terms of primary and secondary variables (including inputs). The function accepts lists of input variables, state variables, elemental and constraint equations, and output expressions.

The functions `stateEquations` and `outputEquations` yield what are in general *nonlinear* state and output equations. Linear state and output equations are typically written in a standard vector form described by matrices `A`, `B`, `C`, and `D` (and sometimes `E` and `F`). The `linearizeState` function accepts lists of input variables, state variables, and the time-derivatives of the state vector (from `stateEquations`) and returns the `A`, `B`, and `E` matrices. Similarly, `linearizeOutput` returns the `C`, `D`, and `F` matrices.

An example of how to use this package is [included](https://github.com/CameronDevine/Statum/blob/master/mathematica/Example.nb).

# Acknowledgments

The authors would like to acknowledge the work of [Gavin Basuel](https://www.gavinbasuel.com/) who designed the user experience for the web interface and helped with HTML/CSS development.

# References

<!--stackedit_data:
eyJkaXNjdXNzaW9ucyI6eyJTUjhYckl2em11VWpGY1paIjp7In
N0YXJ0Ijo4MjgsImVuZCI6OTgzLCJ0ZXh0IjoiV2hlbiBkZXRl
cm1pbmluZyB0aGUgZGlmZmVyZW50aWFsIGVxdWF0aW9uIG9mIG
EgZHluYW1pYyBzeXN0ZW0gdXNpbmcgbGluZWFyIGdyYeKApiJ9
LCJ2QWlBMUtnQUJta1lPY01lIjp7InN0YXJ0IjoyMDk1LCJlbm
QiOjIxMDksInRleHQiOiJCQVNJQyBub3RhdGlvbiJ9fSwiY29t
bWVudHMiOnsiUnlMamsycUxjcjhEczhKZCI6eyJkaXNjdXNzaW
9uSWQiOiJTUjhYckl2em11VWpGY1paIiwic3ViIjoiZ286MTAy
OTA1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6IkknbSBhIGJpZy
BiZWxpZXZlciB0aGF0IHlvdXIgZmlyc3Qgc2VudGVuY2Ugc2hv
dWxkIHRyeSB0byBjb252ZXkgdGhlIG1haW4gcG9pbnQgb2YgeW
91ciBwYXBlci4gVGhpcyBpcyBtb3JlIG9mIGFuIFwiaW50cm9k
dWN0aW9uXCIgc2VjdGlvbiBzZW50ZW5jZSwgYXMgYXJlIHRob3
NlIHRoYXQgZm9sbG93IGl0LiBQZXJoYXBzIHRoaXMgKmlzKiBl
ZmZlY3RpdmVseSB0aGUgaW50cm9kdWN0aW9uIGFuZCB0aGVyZS
dzIGEgc2VwYXJhdGUgYWJzdHJhY3QgLi4uIGlmIHNvLCB0aGF0
J3MgZmluZS4iLCJjcmVhdGVkIjoxNTQzNzE5MTAyODMwfSwiem
Rod2NNWmllRFdySXBrQyI6eyJkaXNjdXNzaW9uSWQiOiJTUjhY
ckl2em11VWpGY1paIiwic3ViIjoiZ286MTAyOTA1NDM1NTMwOD
k2NDc0ODAwIiwidGV4dCI6IkknbSBnb2luZyB0byBjb250aW51
ZSBjb21tZW50aW5nIGFzIGlmIHRoaXMgdGV4dCBpcyBwcmVjZW
RlZCBieSBhbiBhYnN0cmFjdCBvZiBzb21lIHNvcnQuIiwiY3Jl
YXRlZCI6MTU0MzcxOTIwMTgwOH0sIkV1T1V2YkZpSDVxVG5LUT
AiOnsiZGlzY3Vzc2lvbklkIjoidkFpQTFLZ0FCbWtZT2NNZSIs
InN1YiI6ImdoOjEwMzk0ODk2IiwidGV4dCI6IlNob3VsZCB3ZS
BjaXRlIEJBU0lDIG5vdGF0aW9uPyBJIGZvdW5kIGl0IG9uIFdp
a2lwZWRpYSwgIFxuW2h0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy
93aWtpL0NhbGN1bGF0b3JfaW5wdXRfbWV0aG9kcyNCQVNJQ19u
b3RhdGlvbl0oaHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2
kvQ2FsY3VsYXRvcl9pbnB1dF9tZXRob2RzI0JBU0lDX25vdGF0
aW9uKSIsImNyZWF0ZWQiOjE1NDM5NTM3NTQ2NDl9fSwiaGlzdG
9yeSI6Wy0xODQxMzA1MTc3LC03MzU2MDU0NjUsMTcxNzIwMDA4
NiwtMTUxMzkwNTAwNywyMDIyMjk1Mzc3LC05MjA5Njk2NjMsOD
c0NDAyMTkxLDUyMDIwNzE1NCwtOTM1NjA1MzE1LC0xNzYyMDM3
Mzg4LC01NzUzNDM3MTAsNjcwNDQ3NzEsLTIyOTEzNTc2OSwtMT
EyMzM5MjA1NCwtODg3MzAxODIsMjEwMTkyNDY4NSw2MDIwNzk3
ODAsMTA4NTMwNzM4MiwtMTQ1MTc3OTQyMywtMTAwOTk1ODAyN1
19
-->