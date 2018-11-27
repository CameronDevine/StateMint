---
title: 'Statum: An Application for Determining Symbolic Dynamic System Models using Linear Graph Methods'
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

# Summary

When determining the differential equation of a dynamic system using linear graph methods finding the elemental and constraint equations is the first step.
An understanding of the physical phenomena is necessary to determine these equations.
The next step is to eliminate non state variables from the equations until the minimal set of differential equations remains.
This step is where students most often make a mistake.
When learning system dynamics students work many problems as a part of their coursework.
A reoccuring mistake can greatly effect a students percieved skill in this subject area.
However, this algebra is not a necessary component of a strong understanding of system dynamics.

To aid students in their learning process a program was written to symbolically determine the differential equations using the elemental and constraint equations as input.
This program allows students to focus on the process of creating a dynamic system model without worrying about algabraic mistakes.
This frees the student to work on the aspects of system dynamics which are new and unique.

Because symbolic math libraries already exist, writing this software is a relatively trivial task.
This was originally done in Mathematica because of its advanced symbolic math capabilities.
However, this required students to purchase and install mathematica.
Because of the size and cost of Mathematica a more ecanomical solution was desired.
To solve this problem the Python programming language along with SymPy [@meurer2017], a symbolic math library, was used to recreate the software.
This provides the same functionality without the cost barrier and with a smaller installed size.
The Python implementation also allows this code to be run as an Amazon AWS Lambda function.
With the Lambda function a website can be designed to allow this software to be used by any device with an internet connection and web browser.

# Mathematica Package

The Mathematica package for solving the state model algebra has two algorithms included.
The first is a set of functions which primarily use the `Eliminate` function to remove all unneeded variables.
The primary function takes a list of the equations and the input and output equations and returns the state equation.
This equation can then be linearized using the `linearizeState` function.
The second is a function which roughly replicates the algebra which would be performed by hand.
When using this function the equations provided must be in the form defined by Rowell and Wormley [@rowell1997].
Once the operation is complete the state equation matrices, transfer function, and state equation are returned.
A tutorial on how to use this package is included.

# Python Package

The Python package for performing the same task uses similar logic to the second method of the Mathematica package, again in the form defined by Rowell and Wormley [@rowell1997].
This function returns an object which includes the resulting system as a state space model, a transfer function, and an equation.
Helper functions are included to convert the symbolic matrices to Numpy [@oliphant2015] objects.
This code is documented using [readthedocs.io](https://statum.readthedocs.io/en/latest/) and works for both linear and nonlinear systems.

# Web Interface

To allow those without programming experience to use this code a web interface was designed and [implemented](http://statum.camerondevine.me/).
This interface has text boxes for equation input, and displays results as rendered math or code which can be copied into \LaTeX, Matlab, Python, or Mathematica.
Examples and documentation are built in to make learning how to use the interface as painless as possible.
There is also the ability to share, download, and save the system models for later use or modification.
This interface is designed to run on Amazon AWS serverless resources to simplify upkeep and keep costs low.
An automated installer is also included.

# Acknowledgments

The authors would like to acknowledge the work of [Gavin Basuel](https://www.gavinbasuel.com/) who designed the user experience for the web interface and helped with HTML/CSS development.

# References
