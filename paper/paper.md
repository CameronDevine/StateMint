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
When derived by hand there is a considerable chance of algebraic mistakes while finding these models.
This 

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
N0YXJ0Ijo4ODAsImVuZCI6MTAzNSwidGV4dCI6IldoZW4gZGV0
ZXJtaW5pbmcgdGhlIGRpZmZlcmVudGlhbCBlcXVhdGlvbiBvZi
BhIGR5bmFtaWMgc3lzdGVtIHVzaW5nIGxpbmVhciBncmHigKYi
fSwidkFpQTFLZ0FCbWtZT2NNZSI6eyJzdGFydCI6MjE0NywiZW
5kIjoyMTYxLCJ0ZXh0IjoiQkFTSUMgbm90YXRpb24ifX0sImNv
bW1lbnRzIjp7IlJ5TGprMnFMY3I4RHM4SmQiOnsiZGlzY3Vzc2
lvbklkIjoiU1I4WHJJdnptdVVqRmNaWiIsInN1YiI6ImdvOjEw
MjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOiJJJ20gYSBiaW
cgYmVsaWV2ZXIgdGhhdCB5b3VyIGZpcnN0IHNlbnRlbmNlIHNo
b3VsZCB0cnkgdG8gY29udmV5IHRoZSBtYWluIHBvaW50IG9mIH
lvdXIgcGFwZXIuIFRoaXMgaXMgbW9yZSBvZiBhbiBcImludHJv
ZHVjdGlvblwiIHNlY3Rpb24gc2VudGVuY2UsIGFzIGFyZSB0aG
9zZSB0aGF0IGZvbGxvdyBpdC4gUGVyaGFwcyB0aGlzICppcyog
ZWZmZWN0aXZlbHkgdGhlIGludHJvZHVjdGlvbiBhbmQgdGhlcm
UncyBhIHNlcGFyYXRlIGFic3RyYWN0IC4uLiBpZiBzbywgdGhh
dCdzIGZpbmUuIiwiY3JlYXRlZCI6MTU0MzcxOTEwMjgzMH0sIn
pkaHdjTVppZURXcklwa0MiOnsiZGlzY3Vzc2lvbklkIjoiU1I4
WHJJdnptdVVqRmNaWiIsInN1YiI6ImdvOjEwMjkwNTQzNTUzMD
g5NjQ3NDgwMCIsInRleHQiOiJJJ20gZ29pbmcgdG8gY29udGlu
dWUgY29tbWVudGluZyBhcyBpZiB0aGlzIHRleHQgaXMgcHJlY2
VkZWQgYnkgYW4gYWJzdHJhY3Qgb2Ygc29tZSBzb3J0LiIsImNy
ZWF0ZWQiOjE1NDM3MTkyMDE4MDh9LCJFdU9VdmJGaUg1cVRuS1
EwIjp7ImRpc2N1c3Npb25JZCI6InZBaUExS2dBQm1rWU9jTWUi
LCJzdWIiOiJnaDoxMDM5NDg5NiIsInRleHQiOiJTaG91bGQgd2
UgY2l0ZSBCQVNJQyBub3RhdGlvbj8gSSBmb3VuZCBpdCBvbiBX
aWtpcGVkaWEsICBcbltodHRwczovL2VuLndpa2lwZWRpYS5vcm
cvd2lraS9DYWxjdWxhdG9yX2lucHV0X21ldGhvZHMjQkFTSUNf
bm90YXRpb25dKGh0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy93aW
tpL0NhbGN1bGF0b3JfaW5wdXRfbWV0aG9kcyNCQVNJQ19ub3Rh
dGlvbikiLCJjcmVhdGVkIjoxNTQzOTUzNzU0NjQ5fX0sImhpc3
RvcnkiOlstMTU1OTI5NTUwMCwtNzM1NjA1NDY1LDE3MTcyMDAw
ODYsLTE1MTM5MDUwMDcsMjAyMjI5NTM3NywtOTIwOTY5NjYzLD
g3NDQwMjE5MSw1MjAyMDcxNTQsLTkzNTYwNTMxNSwtMTc2MjAz
NzM4OCwtNTc1MzQzNzEwLDY3MDQ0NzcxLC0yMjkxMzU3NjksLT
ExMjMzOTIwNTQsLTg4NzMwMTgyLDIxMDE5MjQ2ODUsNjAyMDc5
NzgwLDEwODUzMDczODIsLTE0NTE3Nzk0MjMsLTEwMDk5NTgwMj
ddfQ==
-->