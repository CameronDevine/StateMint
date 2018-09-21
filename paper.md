---
title: 'State Model RnD: An Algebra Solver for Dynamic Systems'
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
  - name: University of Washington
    index: 1
  - name: Saint Martin's University
    index: 2
date: 26 September 2018
bibliography: paper.bib
---

# Summary

When solving for the differential equation describing a dynamic system the algebra required can become complex and tedious.
This algebra is one of the areas where students commonly struggle when learning system dynamics, however it is not necessary for curating a conceptual understanding of the topic.
Since this process is relatively easy to automate a solver was written in python.
To allow convenient access without the need to install software locally a web interface was designed and built.
Using this tool students can focus on the important aspects of system dynamics without wading through unnecessary algebra.

# Statement of Need

When creating the differential equation for a dynamic system one must first find the elemental and constraint equations for the system.
This can be quickly and easily accomplished.
However, the ensuing algebra can be tedious and error prone.
Once learned, there is little benefit from doing this algebra by hand.
For students, this is especially true as they solve many homework problems to practice their skills.
A computer algebra system can be used to automate this task and allow students to focus on the important aspects of constructing a dynamic system model.

# Python Package

To find the differential equation from the elemental and constraint equations a Python package was written to perform this algebra using SymPy [@meurer2017].
As input, this package takes the elemental equations of the state variables, the other elemental equations, the constraint equations, the list of input variables, and the list of output variables in the form defined by Rowell and Wormley [@rowell1997].
Once calculations are completed the output includes the state space equation, state and output equations, and transfer function.
This information is more thoroughly documented using [readthedocs.io](https://statemodelrnd.readthedocs.io/en/latest/).
This package works for both linear and nonlinear models.

# Web Interface

To allow those without programming experience to use this code a web interface was designed and [implemented](http://statemodelrnd.camerondevine.me/).
This interface has text boxes for equations to be entered into and displays results as rendered math or code which can be copied into \LaTeX, Matlab, Python, or Mathematica.
There is also the ability to share, download, and save the system models for later use or modification.
This interface is designed to run on Amazon AWS serverless resources to simplify upkeep and keep costs low.

# Acknowledgments

The authors would like to acknowledge the work of [Gavin Basuel](https://www.gavinbasuel.com/) who designed the user experience for the web interface and helped with HTML/CSS development.

# References
