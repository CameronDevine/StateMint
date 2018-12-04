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

# Summary

When determining the differential equation of a dynamic system using linear graph methods finding the elemental and constraint equations is the first step.
The next step is to algebraically eliminate those variables that are not state or input variables from the equations until a minimal set of differential equations remains.
During this step of manually reducing the system of equations is where students often make mistakes, leading to frustration and discouragement.
However, this algebra is not a necessary component of a strong understanding of system dynamics and can be easily automated using tools we present here.


To aid students in their learning process a program was written to symbolically determine the differential equations using the elemental and constraint equations as input.
This program allows students to focus on the process of creating a dynamic system model without worrying about algebraic mistakes.
This allows the student to focus on course content which is new and unique.

Utilizing the advanced symbolic mathematics capabilities of Mathematica, a package was written to determine the differential equation.
However, this requires students to purchase, install, and learn Mathematica, often with a considerable monetary investment and learning curve.
To mitigate these problems a web app was designed to allow students to use this tool without any knowledge of programming by allowing equations to be input in BASIC notation, similar to most scientific calculators.
To support this interface a Python package was written with the same functionality as the Mathematica package.

To solve this problem the Python programming language along with SymPy [@meurer2017], a symbolic math library, was used to recreate the software.
This provides the same functionality without the cost barrier and with a smaller installed size.
The Python implementation also allows this code to be run as an Amazon AWS Lambda function.
With the Lambda function, a website was designed to allow this software to be used with any device which has an internet connection and a web browser.
Because equations are entered in BASIC notation, similar to most scientific calculators, no programming knowledge is needed to use this interface.

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
N0YXJ0Ijo2NjUsImVuZCI6ODIwLCJ0ZXh0IjoiV2hlbiBkZXRl
cm1pbmluZyB0aGUgZGlmZmVyZW50aWFsIGVxdWF0aW9uIG9mIG
EgZHluYW1pYyBzeXN0ZW0gdXNpbmcgbGluZWFyIGdyYeKApiJ9
LCJleVB3U3hGS1pTN3ViaWxuIjp7InN0YXJ0IjoxMTM3LCJlbm
QiOjExMzcsInRleHQiOiJXaGVuIGxlYXJuaW5nIHN5c3RlbSBk
eW5hbWljcywgc3R1ZGVudHMgd29yayBtYW55IHByb2JsZW1zIG
FzIGEgcGFydCBvZiB0aGVpciBj4oCmIn0sImtJdEwxUVZCSEl5
a21UQnQiOnsic3RhcnQiOjEyOTIsImVuZCI6MTQ2MywidGV4dC
I6IlRvIGFpZCBzdHVkZW50cyBpbiB0aGVpciBsZWFybmluZyBw
cm9jZXNzIGEgcHJvZ3JhbSB3YXMgd3JpdHRlbiB0byBzeW1ib2
xpY2FsbHnigKYifSwicngyTHVtZGNLVkVpMmZVSyI6eyJzdGFy
dCI6MjM5MiwiZW5kIjoyMzk2LCJ0ZXh0IjoidXNlZCJ9LCJFVV
JPRjRhRjdCQjd0OERKIjp7InN0YXJ0Ijo0MzAwLCJlbmQiOjQz
OTAsInRleHQiOiJbZG9jdW1lbnRhdGlvbl0oKSJ9LCJ2QWlBMU
tnQUJta1lPY01lIjp7InN0YXJ0IjoyMTA5LCJlbmQiOjIxMjMs
InRleHQiOiJCQVNJQyBub3RhdGlvbiJ9fSwiY29tbWVudHMiOn
siUnlMamsycUxjcjhEczhKZCI6eyJkaXNjdXNzaW9uSWQiOiJT
UjhYckl2em11VWpGY1paIiwic3ViIjoiZ286MTAyOTA1NDM1NT
MwODk2NDc0ODAwIiwidGV4dCI6IkknbSBhIGJpZyBiZWxpZXZl
ciB0aGF0IHlvdXIgZmlyc3Qgc2VudGVuY2Ugc2hvdWxkIHRyeS
B0byBjb252ZXkgdGhlIG1haW4gcG9pbnQgb2YgeW91ciBwYXBl
ci4gVGhpcyBpcyBtb3JlIG9mIGFuIFwiaW50cm9kdWN0aW9uXC
Igc2VjdGlvbiBzZW50ZW5jZSwgYXMgYXJlIHRob3NlIHRoYXQg
Zm9sbG93IGl0LiBQZXJoYXBzIHRoaXMgKmlzKiBlZmZlY3Rpdm
VseSB0aGUgaW50cm9kdWN0aW9uIGFuZCB0aGVyZSdzIGEgc2Vw
YXJhdGUgYWJzdHJhY3QgLi4uIGlmIHNvLCB0aGF0J3MgZmluZS
4iLCJjcmVhdGVkIjoxNTQzNzE5MTAyODMwfSwiemRod2NNWmll
RFdySXBrQyI6eyJkaXNjdXNzaW9uSWQiOiJTUjhYckl2em11VW
pGY1paIiwic3ViIjoiZ286MTAyOTA1NDM1NTMwODk2NDc0ODAw
IiwidGV4dCI6IkknbSBnb2luZyB0byBjb250aW51ZSBjb21tZW
50aW5nIGFzIGlmIHRoaXMgdGV4dCBpcyBwcmVjZWRlZCBieSBh
biBhYnN0cmFjdCBvZiBzb21lIHNvcnQuIiwiY3JlYXRlZCI6MT
U0MzcxOTIwMTgwOH0sInViZHFOaFdTbXRHVWtTV2UiOnsiZGlz
Y3Vzc2lvbklkIjoiZXlQd1N4RktaUzd1YmlsbiIsInN1YiI6Im
dvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOiJJIHRo
aW5rIGFkZGluZyBhIHBocmFzZSB0byB0aGUgcHJlY2VkaW5nIH
NlbnRlbmNlIGNvdWxkIGNhcHR1cmUgd2hhdCB5b3UncmUgdHJ5
aW5nIHRvIHNheSwgaGVyZS4gU29tZXRoaW5nIGxpa2UgXCIuLi
4gbWFrZSBtaXN0YWtlcywgd2hpY2ggbGVhZCB0byBmcnVzdHJh
dGlvbiBhbmQgZGlzY291cmFnZW1lbnQgd2hlbiBtYW51YWxseS
ByZWR1Y2luZyB0aGUgc3lzdGVtIG9mIGVxdWF0aW9ucy5cIiIs
ImNyZWF0ZWQiOjE1NDM3MTk2MTA2ODd9LCI0QnJjTmpzRGx4U2
JMbE02Ijp7ImRpc2N1c3Npb25JZCI6ImtJdEwxUVZCSEl5a21U
QnQiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLC
J0ZXh0IjoiV2UgY2FuIG5vdyBiZSBtb3JlIHNwZWNpZmljLCBo
ZXJlLiBXZSBoYXZlIGFscmVhZHkgaW50cm9kdWNlZCB0aGUgZX
F1YXRpb25zIGFuZCB0aGUgdGFzayBvZiBhdXRvbWF0aW9uLiIs
ImNyZWF0ZWQiOjE1NDM3MjAwNjM2OTJ9LCI0b3hyUnNoRklpY0
0yRU9PIjp7ImRpc2N1c3Npb25JZCI6InJ4Mkx1bWRjS1ZFaTJm
VUsiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLC
J0ZXh0IjoiSXQncyBiZXN0IHRvIGF2b2lkIFwidXNlZFwiIC4u
LiBhbmQgZXZlbiBiZXR0ZXIgdG8gYXZvaWQgdGhlIHBocmFzaW
5nIHRoYXQgbGVhZCB0byBpdC4gRS5nLiB0aGlzIHNlbnRlbmNl
IGNvdWxkIGJlIFwiRm9yIHRoZXNlIHJlYXNvbnMsIGEgdmVyc2
lvbiBvZiB0aGUgc29mdHdhcmUgd3JpdHRlbiBpbiB0aGUgUHl0
aG9uIC4uLi5cIiIsImNyZWF0ZWQiOjE1NDM3MjA2NjU5MDZ9LC
JFdWlEYVhrOW5YZWVtR2pSIjp7ImRpc2N1c3Npb25JZCI6IkVV
Uk9GNGFGN0JCN3Q4REoiLCJzdWIiOiJnbzoxMDI5MDU0MzU1Mz
A4OTY0NzQ4MDAiLCJ0ZXh0IjoiSSdtIGFmcmFpZCB0byBoYXJk
Y29kZSB0aGUgdXJsLCBlc3BlY2lhbGx5IGlmIHdlJ3JlIGNoYW
5naW5nIHRvIFN0YXRlTWludCAuLi4iLCJjcmVhdGVkIjoxNTQz
Nzc2ODIwMjE1fSwiNkJONGM1bXdyVWlGZ2JFQiI6eyJkaXNjdX
NzaW9uSWQiOiJFVVJPRjRhRjdCQjd0OERKIiwic3ViIjoiZ2g6
MTAzOTQ4OTYiLCJ0ZXh0IjoiV2hlbiBJIGNoYW5nZWQgdGhlIG
5hbWUgbGFzdCB0aW1lIEkgZGlkIGEgdGV4dCBzZWFyY2ggaW4g
YWxsIGZpbGVzIGZvciBTdGF0ZU1vZGVsUm5ELiBXaGVuIEkgY2
hhbmdlIHRvIFN0YXRlTWludCBJIGNhbiBzaW1wbHkgc2VhcmNo
IGZvciBhbnkgZmlsZXMgd2hpY2ggaW5jbHVkZSBlaXRoZXIgU3
RhdGVNb2RlbFJuRCBvciBTdGF0dW0gYW5kIGNoYW5nZSB0aG9z
ZS4iLCJjcmVhdGVkIjoxNTQzODgyMDEzODMwfSwiRXVPVXZiRm
lINXFUbktRMCI6eyJkaXNjdXNzaW9uSWQiOiJ2QWlBMUtnQUJt
a1lPY01lIiwic3ViIjoiZ2g6MTAzOTQ4OTYiLCJ0ZXh0IjoiU2
hvdWxkIHdlIGNpdGUgQkFTSUMgbm90YXRpb24/IEkgZm91bmQg
aXQgb24gV2lraXBlZGlhLCAgXG5baHR0cHM6Ly9lbi53aWtpcG
VkaWEub3JnL3dpa2kvQ2FsY3VsYXRvcl9pbnB1dF9tZXRob2Rz
I0JBU0lDX25vdGF0aW9uXShodHRwczovL2VuLndpa2lwZWRpYS
5vcmcvd2lraS9DYWxjdWxhdG9yX2lucHV0X21ldGhvZHMjQkFT
SUNfbm90YXRpb24pIiwiY3JlYXRlZCI6MTU0Mzk1Mzc1NDY0OX
19LCJoaXN0b3J5IjpbNjcwNDQ3NzEsLTIyOTEzNTc2OSwtMTEy
MzM5MjA1NCwtODg3MzAxODIsMjEwMTkyNDY4NSw2MDIwNzk3OD
AsMTA4NTMwNzM4MiwtMTQ1MTc3OTQyMywtMTAwOTk1ODAyNyw0
ODQyNDgyMTgsMTEzMjIyMzg5MywtNTYwMzg3MjU1LC0zMzI2Mj
E3MDYsMTY4MjUzMDQ5MywtMTQ5MjkwOTU3LDQyMzY2MDExLC0y
NTY5NjU4MzcsLTEyMDE5MTA0NTIsMjA5ODc3NTk2MF19
-->