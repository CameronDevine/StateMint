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
This was originally done in Mathematica because of its advanced symbolic math capabilities.
However, this required students to purchase and install Mathematica.
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
xpY2FsbHnigKYifSwiUXdMRHYzSDNCTVBMVUw1MCI6eyJzdGFy
dCI6MTkxMywiZW5kIjoxOTIxLCJ0ZXh0IjoicmVxdWlyZWQifS
wicFJLVGlub0tnc1c3VnQySCI6eyJzdGFydCI6MTk4MywiZW5k
IjoxOTk2LCJ0ZXh0Ijoic2l6ZSBhbmQgY29zdCJ9LCJyeDJMdW
1kY0tWRWkyZlVLIjp7InN0YXJ0IjoyMTY3LCJlbmQiOjIxNzEs
InRleHQiOiJ1c2VkIn0sIkVVUk9GNGFGN0JCN3Q4REoiOnsic3
RhcnQiOjQwNzUsImVuZCI6NDE2NSwidGV4dCI6Iltkb2N1bWVu
dGF0aW9uXSgpIn0sImZXZW9pd3plaEVlUjVDU3EiOnsic3Rhcn
QiOjI1NzEsImVuZCI6MjU4NSwidGV4dCI6IkJBU0lDIG5vdGF0
aW9uIn19LCJjb21tZW50cyI6eyJSeUxqazJxTGNyOERzOEpkIj
p7ImRpc2N1c3Npb25JZCI6IlNSOFhySXZ6bXVVakZjWloiLCJz
dWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZXh0Ij
oiSSdtIGEgYmlnIGJlbGlldmVyIHRoYXQgeW91ciBmaXJzdCBz
ZW50ZW5jZSBzaG91bGQgdHJ5IHRvIGNvbnZleSB0aGUgbWFpbi
Bwb2ludCBvZiB5b3VyIHBhcGVyLiBUaGlzIGlzIG1vcmUgb2Yg
YW4gXCJpbnRyb2R1Y3Rpb25cIiBzZWN0aW9uIHNlbnRlbmNlLC
BhcyBhcmUgdGhvc2UgdGhhdCBmb2xsb3cgaXQuIFBlcmhhcHMg
dGhpcyAqaXMqIGVmZmVjdGl2ZWx5IHRoZSBpbnRyb2R1Y3Rpb2
4gYW5kIHRoZXJlJ3MgYSBzZXBhcmF0ZSBhYnN0cmFjdCAuLi4g
aWYgc28sIHRoYXQncyBmaW5lLiIsImNyZWF0ZWQiOjE1NDM3MT
kxMDI4MzB9LCJ6ZGh3Y01aaWVEV3JJcGtDIjp7ImRpc2N1c3Np
b25JZCI6IlNSOFhySXZ6bXVVakZjWloiLCJzdWIiOiJnbzoxMD
I5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZXh0IjoiSSdtIGdvaW5n
IHRvIGNvbnRpbnVlIGNvbW1lbnRpbmcgYXMgaWYgdGhpcyB0ZX
h0IGlzIHByZWNlZGVkIGJ5IGFuIGFic3RyYWN0IG9mIHNvbWUg
c29ydC4iLCJjcmVhdGVkIjoxNTQzNzE5MjAxODA4fSwidWJkcU
5oV1NtdEdVa1NXZSI6eyJkaXNjdXNzaW9uSWQiOiJleVB3U3hG
S1pTN3ViaWxuIiwic3ViIjoiZ286MTAyOTA1NDM1NTMwODk2ND
c0ODAwIiwidGV4dCI6IkkgdGhpbmsgYWRkaW5nIGEgcGhyYXNl
IHRvIHRoZSBwcmVjZWRpbmcgc2VudGVuY2UgY291bGQgY2FwdH
VyZSB3aGF0IHlvdSdyZSB0cnlpbmcgdG8gc2F5LCBoZXJlLiBT
b21ldGhpbmcgbGlrZSBcIi4uLiBtYWtlIG1pc3Rha2VzLCB3aG
ljaCBsZWFkIHRvIGZydXN0cmF0aW9uIGFuZCBkaXNjb3VyYWdl
bWVudCB3aGVuIG1hbnVhbGx5IHJlZHVjaW5nIHRoZSBzeXN0ZW
0gb2YgZXF1YXRpb25zLlwiIiwiY3JlYXRlZCI6MTU0MzcxOTYx
MDY4N30sIjRCcmNOanNEbHhTYkxsTTYiOnsiZGlzY3Vzc2lvbk
lkIjoia0l0TDFRVkJISXlrbVRCdCIsInN1YiI6ImdvOjEwMjkw
NTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOiJXZSBjYW4gbm93IG
JlIG1vcmUgc3BlY2lmaWMsIGhlcmUuIFdlIGhhdmUgYWxyZWFk
eSBpbnRyb2R1Y2VkIHRoZSBlcXVhdGlvbnMgYW5kIHRoZSB0YX
NrIG9mIGF1dG9tYXRpb24uIiwiY3JlYXRlZCI6MTU0MzcyMDA2
MzY5Mn0sInR3WmZ5RnhIVms0ZnZpbUQiOnsiZGlzY3Vzc2lvbk
lkIjoiUXdMRHYzSDNCTVBMVUw1MCIsInN1YiI6ImdvOjEwMjkw
NTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOiJJIHRoaW5rIHByZX
NlbnQgdGVuc2UgaXMgYmV0dGVyIHNpbmNlIHdlJ3JlIHN0aWxs
IHJlbGVhc2luZyBhIE1NQSBwYWNrYWdlIiwiY3JlYXRlZCI6MT
U0MzcyMDMzMzU0OH0sImtuWklSeWw3UnJFWFVUMzYiOnsiZGlz
Y3Vzc2lvbklkIjoicFJLVGlub0tnc1c3VnQySCIsInN1YiI6Im
dvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOiJJIHRo
aW5rIHBlcmhhcHMgdGhlIG1vc3QgaW1wb3J0YW50IGFzcGVjdC
BpcyB0aGF0IGl0IHJlcXVpcmVzIHN0dWRlbnRzIHRvIGxlYXJu
IGEgbmV3IHNvZnR3YXJlIHN5c3RlbSAuLi4gd2hpY2ggbW9yZS
B0aGFuIG91dHdlaWdocyB0aGUgYWR2YW50YWdlcyBmb3IgbW9z
dCBvZiB0aGUgc3R1ZGVudHMgLi4uIHlvdXIgd2ViIGFwcCBsZX
RzIHRoZW0gZ2V0IHN0YXJ0ZWQgd2l0aG91dCBsZWFybmluZyBN
TUEiLCJjcmVhdGVkIjoxNTQzNzIwNDQ1Njc4fSwiNG94clJzaE
ZJaWNNMkVPTyI6eyJkaXNjdXNzaW9uSWQiOiJyeDJMdW1kY0tW
RWkyZlVLIiwic3ViIjoiZ286MTAyOTA1NDM1NTMwODk2NDc0OD
AwIiwidGV4dCI6Ikl0J3MgYmVzdCB0byBhdm9pZCBcInVzZWRc
IiAuLi4gYW5kIGV2ZW4gYmV0dGVyIHRvIGF2b2lkIHRoZSBwaH
Jhc2luZyB0aGF0IGxlYWQgdG8gaXQuIEUuZy4gdGhpcyBzZW50
ZW5jZSBjb3VsZCBiZSBcIkZvciB0aGVzZSByZWFzb25zLCBhIH
ZlcnNpb24gb2YgdGhlIHNvZnR3YXJlIHdyaXR0ZW4gaW4gdGhl
IFB5dGhvbiAuLi4uXCIiLCJjcmVhdGVkIjoxNTQzNzIwNjY1OT
A2fSwiRXVpRGFYazluWGVlbUdqUiI6eyJkaXNjdXNzaW9uSWQi
OiJFVVJPRjRhRjdCQjd0OERKIiwic3ViIjoiZ286MTAyOTA1ND
M1NTMwODk2NDc0ODAwIiwidGV4dCI6IkknbSBhZnJhaWQgdG8g
aGFyZGNvZGUgdGhlIHVybCwgZXNwZWNpYWxseSBpZiB3ZSdyZS
BjaGFuZ2luZyB0byBTdGF0ZU1pbnQgLi4uIiwiY3JlYXRlZCI6
MTU0Mzc3NjgyMDIxNX0sIjZCTjRjNW13clVpRmdiRUIiOnsiZG
lzY3Vzc2lvbklkIjoiRVVST0Y0YUY3QkI3dDhESiIsInN1YiI6
ImdoOjEwMzk0ODk2IiwidGV4dCI6IldoZW4gSSBjaGFuZ2VkIH
RoZSBuYW1lIGxhc3QgdGltZSBJIGRpZCBhIHRleHQgc2VhcmNo
IGluIGFsbCBmaWxlcyBmb3IgU3RhdGVNb2RlbFJuRC4gV2hlbi
BJIGNoYW5nZSB0byBTdGF0ZU1pbnQgSSBjYW4gc2ltcGx5IHNl
YXJjaCBmb3IgYW55IGZpbGVzIHdoaWNoIGluY2x1ZGUgZWl0aG
VyIFN0YXRlTW9kZWxSbkQgb3IgU3RhdHVtIGFuZCBjaGFuZ2Ug
dGhvc2UuIiwiY3JlYXRlZCI6MTU0Mzg4MjAxMzgzMH0sIm9FOU
lBTmxJUTVNWnZoQWUiOnsiZGlzY3Vzc2lvbklkIjoiZldlb2l3
emVoRWVSNUNTcSIsInN1YiI6ImdoOjEwMzk0ODk2IiwidGV4dC
I6IlNob3VsZCB3ZSBjaXRlIEJBU0lDIG5vdGF0aW9uPyBJIGZv
dW5kIGl0IG9uIFdpa2lwZWRpYSxcbmh0dHBzOi8vZW4ud2lraX
BlZGlhLm9yZy93aWtpL0NhbGN1bGF0b3JfaW5wdXRfbWV0aG9k
cyNCQVNJQ19ub3RhdGlvbiIsImNyZWF0ZWQiOjE1NDM4OTczMz
M3OTN9fSwiaGlzdG9yeSI6WzIyNDMwMTUxLDIxMDE5MjQ2ODUs
NjAyMDc5NzgwLDEwODUzMDczODIsLTE0NTE3Nzk0MjMsLTEwMD
k5NTgwMjcsNDg0MjQ4MjE4LDExMzIyMjM4OTMsLTU2MDM4NzI1
NSwtMzMyNjIxNzA2LDE2ODI1MzA0OTMsLTE0OTI5MDk1Nyw0Mj
M2NjAxMSwtMjU2OTY1ODM3LC0xMjAxOTEwNDUyLDIwOTg3NzU5
NjBdfQ==
-->