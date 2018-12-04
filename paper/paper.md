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
To mi
Because of the size and cost of Mathematica a more economical solution was desired.
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
xpY2FsbHnigKYifSwicFJLVGlub0tnc1c3VnQySCI6eyJzdGFy
dCI6MTk3MSwiZW5kIjoxOTg0LCJ0ZXh0Ijoic2l6ZSBhbmQgY2
9zdCJ9LCJyeDJMdW1kY0tWRWkyZlVLIjp7InN0YXJ0IjoyMTU1
LCJlbmQiOjIxNTksInRleHQiOiJ1c2VkIn0sIkVVUk9GNGFGN0
JCN3Q4REoiOnsic3RhcnQiOjQwNjMsImVuZCI6NDE1MywidGV4
dCI6Iltkb2N1bWVudGF0aW9uXSgpIn0sImZXZW9pd3plaEVlUj
VDU3EiOnsic3RhcnQiOjI1NTksImVuZCI6MjU3MywidGV4dCI6
IkJBU0lDIG5vdGF0aW9uIn19LCJjb21tZW50cyI6eyJSeUxqaz
JxTGNyOERzOEpkIjp7ImRpc2N1c3Npb25JZCI6IlNSOFhySXZ6
bXVVakZjWloiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0Nz
Q4MDAiLCJ0ZXh0IjoiSSdtIGEgYmlnIGJlbGlldmVyIHRoYXQg
eW91ciBmaXJzdCBzZW50ZW5jZSBzaG91bGQgdHJ5IHRvIGNvbn
ZleSB0aGUgbWFpbiBwb2ludCBvZiB5b3VyIHBhcGVyLiBUaGlz
IGlzIG1vcmUgb2YgYW4gXCJpbnRyb2R1Y3Rpb25cIiBzZWN0aW
9uIHNlbnRlbmNlLCBhcyBhcmUgdGhvc2UgdGhhdCBmb2xsb3cg
aXQuIFBlcmhhcHMgdGhpcyAqaXMqIGVmZmVjdGl2ZWx5IHRoZS
BpbnRyb2R1Y3Rpb24gYW5kIHRoZXJlJ3MgYSBzZXBhcmF0ZSBh
YnN0cmFjdCAuLi4gaWYgc28sIHRoYXQncyBmaW5lLiIsImNyZW
F0ZWQiOjE1NDM3MTkxMDI4MzB9LCJ6ZGh3Y01aaWVEV3JJcGtD
Ijp7ImRpc2N1c3Npb25JZCI6IlNSOFhySXZ6bXVVakZjWloiLC
JzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZXh0
IjoiSSdtIGdvaW5nIHRvIGNvbnRpbnVlIGNvbW1lbnRpbmcgYX
MgaWYgdGhpcyB0ZXh0IGlzIHByZWNlZGVkIGJ5IGFuIGFic3Ry
YWN0IG9mIHNvbWUgc29ydC4iLCJjcmVhdGVkIjoxNTQzNzE5Mj
AxODA4fSwidWJkcU5oV1NtdEdVa1NXZSI6eyJkaXNjdXNzaW9u
SWQiOiJleVB3U3hGS1pTN3ViaWxuIiwic3ViIjoiZ286MTAyOT
A1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6IkkgdGhpbmsgYWRk
aW5nIGEgcGhyYXNlIHRvIHRoZSBwcmVjZWRpbmcgc2VudGVuY2
UgY291bGQgY2FwdHVyZSB3aGF0IHlvdSdyZSB0cnlpbmcgdG8g
c2F5LCBoZXJlLiBTb21ldGhpbmcgbGlrZSBcIi4uLiBtYWtlIG
1pc3Rha2VzLCB3aGljaCBsZWFkIHRvIGZydXN0cmF0aW9uIGFu
ZCBkaXNjb3VyYWdlbWVudCB3aGVuIG1hbnVhbGx5IHJlZHVjaW
5nIHRoZSBzeXN0ZW0gb2YgZXF1YXRpb25zLlwiIiwiY3JlYXRl
ZCI6MTU0MzcxOTYxMDY4N30sIjRCcmNOanNEbHhTYkxsTTYiOn
siZGlzY3Vzc2lvbklkIjoia0l0TDFRVkJISXlrbVRCdCIsInN1
YiI6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOi
JXZSBjYW4gbm93IGJlIG1vcmUgc3BlY2lmaWMsIGhlcmUuIFdl
IGhhdmUgYWxyZWFkeSBpbnRyb2R1Y2VkIHRoZSBlcXVhdGlvbn
MgYW5kIHRoZSB0YXNrIG9mIGF1dG9tYXRpb24uIiwiY3JlYXRl
ZCI6MTU0MzcyMDA2MzY5Mn0sImtuWklSeWw3UnJFWFVUMzYiOn
siZGlzY3Vzc2lvbklkIjoicFJLVGlub0tnc1c3VnQySCIsInN1
YiI6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOi
JJIHRoaW5rIHBlcmhhcHMgdGhlIG1vc3QgaW1wb3J0YW50IGFz
cGVjdCBpcyB0aGF0IGl0IHJlcXVpcmVzIHN0dWRlbnRzIHRvIG
xlYXJuIGEgbmV3IHNvZnR3YXJlIHN5c3RlbSAuLi4gd2hpY2gg
bW9yZSB0aGFuIG91dHdlaWdocyB0aGUgYWR2YW50YWdlcyBmb3
IgbW9zdCBvZiB0aGUgc3R1ZGVudHMgLi4uIHlvdXIgd2ViIGFw
cCBsZXRzIHRoZW0gZ2V0IHN0YXJ0ZWQgd2l0aG91dCBsZWFybm
luZyBNTUEiLCJjcmVhdGVkIjoxNTQzNzIwNDQ1Njc4fSwiNG94
clJzaEZJaWNNMkVPTyI6eyJkaXNjdXNzaW9uSWQiOiJyeDJMdW
1kY0tWRWkyZlVLIiwic3ViIjoiZ286MTAyOTA1NDM1NTMwODk2
NDc0ODAwIiwidGV4dCI6Ikl0J3MgYmVzdCB0byBhdm9pZCBcIn
VzZWRcIiAuLi4gYW5kIGV2ZW4gYmV0dGVyIHRvIGF2b2lkIHRo
ZSBwaHJhc2luZyB0aGF0IGxlYWQgdG8gaXQuIEUuZy4gdGhpcy
BzZW50ZW5jZSBjb3VsZCBiZSBcIkZvciB0aGVzZSByZWFzb25z
LCBhIHZlcnNpb24gb2YgdGhlIHNvZnR3YXJlIHdyaXR0ZW4gaW
4gdGhlIFB5dGhvbiAuLi4uXCIiLCJjcmVhdGVkIjoxNTQzNzIw
NjY1OTA2fSwiRXVpRGFYazluWGVlbUdqUiI6eyJkaXNjdXNzaW
9uSWQiOiJFVVJPRjRhRjdCQjd0OERKIiwic3ViIjoiZ286MTAy
OTA1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6IkknbSBhZnJhaW
QgdG8gaGFyZGNvZGUgdGhlIHVybCwgZXNwZWNpYWxseSBpZiB3
ZSdyZSBjaGFuZ2luZyB0byBTdGF0ZU1pbnQgLi4uIiwiY3JlYX
RlZCI6MTU0Mzc3NjgyMDIxNX0sIjZCTjRjNW13clVpRmdiRUIi
OnsiZGlzY3Vzc2lvbklkIjoiRVVST0Y0YUY3QkI3dDhESiIsIn
N1YiI6ImdoOjEwMzk0ODk2IiwidGV4dCI6IldoZW4gSSBjaGFu
Z2VkIHRoZSBuYW1lIGxhc3QgdGltZSBJIGRpZCBhIHRleHQgc2
VhcmNoIGluIGFsbCBmaWxlcyBmb3IgU3RhdGVNb2RlbFJuRC4g
V2hlbiBJIGNoYW5nZSB0byBTdGF0ZU1pbnQgSSBjYW4gc2ltcG
x5IHNlYXJjaCBmb3IgYW55IGZpbGVzIHdoaWNoIGluY2x1ZGUg
ZWl0aGVyIFN0YXRlTW9kZWxSbkQgb3IgU3RhdHVtIGFuZCBjaG
FuZ2UgdGhvc2UuIiwiY3JlYXRlZCI6MTU0Mzg4MjAxMzgzMH0s
Im9FOUlBTmxJUTVNWnZoQWUiOnsiZGlzY3Vzc2lvbklkIjoiZl
dlb2l3emVoRWVSNUNTcSIsInN1YiI6ImdoOjEwMzk0ODk2Iiwi
dGV4dCI6IlNob3VsZCB3ZSBjaXRlIEJBU0lDIG5vdGF0aW9uPy
BJIGZvdW5kIGl0IG9uIFdpa2lwZWRpYSxcbmh0dHBzOi8vZW4u
d2lraXBlZGlhLm9yZy93aWtpL0NhbGN1bGF0b3JfaW5wdXRfbW
V0aG9kcyNCQVNJQ19ub3RhdGlvbiIsImNyZWF0ZWQiOjE1NDM4
OTczMzM3OTN9fSwiaGlzdG9yeSI6Wzg1NTY5ODgwMywtODg3Mz
AxODIsMjEwMTkyNDY4NSw2MDIwNzk3ODAsMTA4NTMwNzM4Miwt
MTQ1MTc3OTQyMywtMTAwOTk1ODAyNyw0ODQyNDgyMTgsMTEzMj
IyMzg5MywtNTYwMzg3MjU1LC0zMzI2MjE3MDYsMTY4MjUzMDQ5
MywtMTQ5MjkwOTU3LDQyMzY2MDExLC0yNTY5NjU4MzcsLTEyMD
E5MTA0NTIsMjA5ODc3NTk2MF19
-->