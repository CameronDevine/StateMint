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
differential equation of a dynamic system using linear graph methods finding the elemental and constraint equations is the first step.
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

The [web interface](http://statemint.camerondevine.me/) has text boxes for equations to be input.
These equations must be entered in the form defined by Rowell and Wormley [@rowell1997].
Once entered, the equations are sent to the Lambda function and the dynamic system model is returned.
The results are then displayed as rendered math or code which can be copied into \LaTeX, Matlab, Python, or Mathematica.
Examples and documentation are built in to make learning how to use the interface as painless as possible.
There is also the ability to share, download, and save the dynamic system models for later use or modification.
Because this interface utilizes Amazon AWS serverless resources, required maintenance and costs are minimized.
An automated installer is also [included](https://github.com/CameronDevine/StateMint/tree/master/web).

# Python Package

The Python package uses the SymPy [@meurer2017] library to symbolically eliminate the unneeded variables.
This function returns an object which includes the resulting system as a state space model, a transfer function, and an equation.
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
RleHQiOiJCQVNJQyBub3RhdGlvbiIsInN0YXJ0IjoyNjAxLCJl
bmQiOjI2MTV9fSwiY29tbWVudHMiOnsiRXVPVXZiRmlINXFUbk
tRMCI6eyJkaXNjdXNzaW9uSWQiOiJ2QWlBMUtnQUJta1lPY01l
Iiwic3ViIjoiZ2g6MTAzOTQ4OTYiLCJ0ZXh0IjoiU2hvdWxkIH
dlIGNpdGUgQkFTSUMgbm90YXRpb24/IEkgZm91bmQgaXQgb24g
V2lraXBlZGlhLCAgXG5baHR0cHM6Ly9lbi53aWtpcGVkaWEub3
JnL3dpa2kvQ2FsY3VsYXRvcl9pbnB1dF9tZXRob2RzI0JBU0lD
X25vdGF0aW9uXShodHRwczovL2VuLndpa2lwZWRpYS5vcmcvd2
lraS9DYWxjdWxhdG9yX2lucHV0X21ldGhvZHMjQkFTSUNfbm90
YXRpb24pIiwiY3JlYXRlZCI6MTU0Mzk1Mzc1NDY0OX19LCJoaX
N0b3J5IjpbLTUzMDU3MzUzNSw0MzM3NDQ2OTMsLTM4NzUzMjky
MCwzMjMzMjY2ODQsNTEyNjA5NTk2LC0xOTQ5NDEzNjAyLC00Mj
IwNDE1OTUsLTE2NTU1Njg0MTQsLTEyMDk3NTA3OTYsLTczNTYw
NTQ2NSwxNzE3MjAwMDg2LC0xNTEzOTA1MDA3LDIwMjIyOTUzNz
csLTkyMDk2OTY2Myw4NzQ0MDIxOTEsNTIwMjA3MTU0LC05MzU2
MDUzMTUsLTE3NjIwMzczODgsLTU3NTM0MzcxMCw2NzA0NDc3MV
19
-->