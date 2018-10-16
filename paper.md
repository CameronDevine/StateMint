---
title: 'StateMint: An Application for Determining Symbolic Dynamic System Models using Linear Graphs Methods'
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

When finding the differential equation of a dynamic system the elemental and constraint equations must be found.
This step requires an understanding of the physical phenomena and how the elements are connected to determine the elemental equations, and constrain equations respectively.
The ensuing algebra to combine these equations can be tedious and error prone.
This algebra is one of the areas where students commonly struggle when learning system dynamics.
Because students solve many problems to learn the process this can greatly affect a students further interest and perceived skill with system dynamics.
However performing this algebra is not a necessary component of a strong understanding of system dynamics.

Because symbolic math libraries already exist, writing software to automatically perform this algebra is relatively trivial task.
This was originally written in Mathematica because of its advanced symbolic math capabilities.
Since the powerful symbolic math library, SymPy [@meurer2017], is available for Python, it was chosen for an open source implementation of this software.
This implementation is especially useful because it can be run as an Amazon AWS Lambda function.
This allowed a web interface to be created which allows students to use the software without the need to install specialized software on their computers.

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
This code is documented using [readthedocs.io](https://statemodelrnd.readthedocs.io/en/latest/) and works for both linear and nonlinear systems.

# Web Interface

To allow those without programming experience to use this code a web interface was designed and [implemented](http://statemodelrnd.camerondevine.me/).
This interface has text boxes for equation input, and displays results as rendered math or code which can be copied into \LaTeX, Matlab, Python, or Mathematica.
Examples and documentation are built in to make learning how to use the interface as painless as possible.
There is also the ability to share, download, and save the system models for later use or modification.
This interface is designed to run on Amazon AWS serverless resources to simplify upkeep and keep costs low.
An automated installer is also included.

# Acknowledgments

The authors would like to acknowledge the work of [Gavin Basuel](https://www.gavinbasuel.com/) who designed the user experience for the web interface and helped with HTML/CSS development.

# References
