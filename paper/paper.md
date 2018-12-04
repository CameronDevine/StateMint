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
To mitigate these problems a web app was designed to allow students to use this tool without any knowledge of programming.
The web app allows equations to be input in BASIC notation, similar to most scientific calculators
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
dCI6MjE4NywiZW5kIjoyMjAwLCJ0ZXh0Ijoic2l6ZSBhbmQgY2
9zdCJ9LCJyeDJMdW1kY0tWRWkyZlVLIjp7InN0YXJ0IjoyMzcx
LCJlbmQiOjIzNzUsInRleHQiOiJ1c2VkIn0sIkVVUk9GNGFGN0
JCN3Q4REoiOnsic3RhcnQiOjQyNzksImVuZCI6NDM2OSwidGV4
dCI6Iltkb2N1bWVudGF0aW9uXSgpIn0sImZXZW9pd3plaEVlUj
VDU3EiOnsic3RhcnQiOjI3NzUsImVuZCI6Mjc4OSwidGV4dCI6
IkJBU0lDIG5vdGF0aW9uIn0sInZBaUExS2dBQm1rWU9jTWUiOn
sic3RhcnQiOjIxMTcsImVuZCI6MjEzMSwidGV4dCI6IkJBU0lD
IG5vdGF0aW9uIn19LCJjb21tZW50cyI6eyJSeUxqazJxTGNyOE
RzOEpkIjp7ImRpc2N1c3Npb25JZCI6IlNSOFhySXZ6bXVVakZj
WloiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLC
J0ZXh0IjoiSSdtIGEgYmlnIGJlbGlldmVyIHRoYXQgeW91ciBm
aXJzdCBzZW50ZW5jZSBzaG91bGQgdHJ5IHRvIGNvbnZleSB0aG
UgbWFpbiBwb2ludCBvZiB5b3VyIHBhcGVyLiBUaGlzIGlzIG1v
cmUgb2YgYW4gXCJpbnRyb2R1Y3Rpb25cIiBzZWN0aW9uIHNlbn
RlbmNlLCBhcyBhcmUgdGhvc2UgdGhhdCBmb2xsb3cgaXQuIFBl
cmhhcHMgdGhpcyAqaXMqIGVmZmVjdGl2ZWx5IHRoZSBpbnRyb2
R1Y3Rpb24gYW5kIHRoZXJlJ3MgYSBzZXBhcmF0ZSBhYnN0cmFj
dCAuLi4gaWYgc28sIHRoYXQncyBmaW5lLiIsImNyZWF0ZWQiOj
E1NDM3MTkxMDI4MzB9LCJ6ZGh3Y01aaWVEV3JJcGtDIjp7ImRp
c2N1c3Npb25JZCI6IlNSOFhySXZ6bXVVakZjWloiLCJzdWIiOi
JnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZXh0IjoiSSdt
IGdvaW5nIHRvIGNvbnRpbnVlIGNvbW1lbnRpbmcgYXMgaWYgdG
hpcyB0ZXh0IGlzIHByZWNlZGVkIGJ5IGFuIGFic3RyYWN0IG9m
IHNvbWUgc29ydC4iLCJjcmVhdGVkIjoxNTQzNzE5MjAxODA4fS
widWJkcU5oV1NtdEdVa1NXZSI6eyJkaXNjdXNzaW9uSWQiOiJl
eVB3U3hGS1pTN3ViaWxuIiwic3ViIjoiZ286MTAyOTA1NDM1NT
MwODk2NDc0ODAwIiwidGV4dCI6IkkgdGhpbmsgYWRkaW5nIGEg
cGhyYXNlIHRvIHRoZSBwcmVjZWRpbmcgc2VudGVuY2UgY291bG
QgY2FwdHVyZSB3aGF0IHlvdSdyZSB0cnlpbmcgdG8gc2F5LCBo
ZXJlLiBTb21ldGhpbmcgbGlrZSBcIi4uLiBtYWtlIG1pc3Rha2
VzLCB3aGljaCBsZWFkIHRvIGZydXN0cmF0aW9uIGFuZCBkaXNj
b3VyYWdlbWVudCB3aGVuIG1hbnVhbGx5IHJlZHVjaW5nIHRoZS
BzeXN0ZW0gb2YgZXF1YXRpb25zLlwiIiwiY3JlYXRlZCI6MTU0
MzcxOTYxMDY4N30sIjRCcmNOanNEbHhTYkxsTTYiOnsiZGlzY3
Vzc2lvbklkIjoia0l0TDFRVkJISXlrbVRCdCIsInN1YiI6Imdv
OjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOiJXZSBjYW
4gbm93IGJlIG1vcmUgc3BlY2lmaWMsIGhlcmUuIFdlIGhhdmUg
YWxyZWFkeSBpbnRyb2R1Y2VkIHRoZSBlcXVhdGlvbnMgYW5kIH
RoZSB0YXNrIG9mIGF1dG9tYXRpb24uIiwiY3JlYXRlZCI6MTU0
MzcyMDA2MzY5Mn0sImtuWklSeWw3UnJFWFVUMzYiOnsiZGlzY3
Vzc2lvbklkIjoicFJLVGlub0tnc1c3VnQySCIsInN1YiI6Imdv
OjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOiJJIHRoaW
5rIHBlcmhhcHMgdGhlIG1vc3QgaW1wb3J0YW50IGFzcGVjdCBp
cyB0aGF0IGl0IHJlcXVpcmVzIHN0dWRlbnRzIHRvIGxlYXJuIG
EgbmV3IHNvZnR3YXJlIHN5c3RlbSAuLi4gd2hpY2ggbW9yZSB0
aGFuIG91dHdlaWdocyB0aGUgYWR2YW50YWdlcyBmb3IgbW9zdC
BvZiB0aGUgc3R1ZGVudHMgLi4uIHlvdXIgd2ViIGFwcCBsZXRz
IHRoZW0gZ2V0IHN0YXJ0ZWQgd2l0aG91dCBsZWFybmluZyBNTU
EiLCJjcmVhdGVkIjoxNTQzNzIwNDQ1Njc4fSwiNG94clJzaEZJ
aWNNMkVPTyI6eyJkaXNjdXNzaW9uSWQiOiJyeDJMdW1kY0tWRW
kyZlVLIiwic3ViIjoiZ286MTAyOTA1NDM1NTMwODk2NDc0ODAw
IiwidGV4dCI6Ikl0J3MgYmVzdCB0byBhdm9pZCBcInVzZWRcIi
AuLi4gYW5kIGV2ZW4gYmV0dGVyIHRvIGF2b2lkIHRoZSBwaHJh
c2luZyB0aGF0IGxlYWQgdG8gaXQuIEUuZy4gdGhpcyBzZW50ZW
5jZSBjb3VsZCBiZSBcIkZvciB0aGVzZSByZWFzb25zLCBhIHZl
cnNpb24gb2YgdGhlIHNvZnR3YXJlIHdyaXR0ZW4gaW4gdGhlIF
B5dGhvbiAuLi4uXCIiLCJjcmVhdGVkIjoxNTQzNzIwNjY1OTA2
fSwiRXVpRGFYazluWGVlbUdqUiI6eyJkaXNjdXNzaW9uSWQiOi
JFVVJPRjRhRjdCQjd0OERKIiwic3ViIjoiZ286MTAyOTA1NDM1
NTMwODk2NDc0ODAwIiwidGV4dCI6IkknbSBhZnJhaWQgdG8gaG
FyZGNvZGUgdGhlIHVybCwgZXNwZWNpYWxseSBpZiB3ZSdyZSBj
aGFuZ2luZyB0byBTdGF0ZU1pbnQgLi4uIiwiY3JlYXRlZCI6MT
U0Mzc3NjgyMDIxNX0sIjZCTjRjNW13clVpRmdiRUIiOnsiZGlz
Y3Vzc2lvbklkIjoiRVVST0Y0YUY3QkI3dDhESiIsInN1YiI6Im
doOjEwMzk0ODk2IiwidGV4dCI6IldoZW4gSSBjaGFuZ2VkIHRo
ZSBuYW1lIGxhc3QgdGltZSBJIGRpZCBhIHRleHQgc2VhcmNoIG
luIGFsbCBmaWxlcyBmb3IgU3RhdGVNb2RlbFJuRC4gV2hlbiBJ
IGNoYW5nZSB0byBTdGF0ZU1pbnQgSSBjYW4gc2ltcGx5IHNlYX
JjaCBmb3IgYW55IGZpbGVzIHdoaWNoIGluY2x1ZGUgZWl0aGVy
IFN0YXRlTW9kZWxSbkQgb3IgU3RhdHVtIGFuZCBjaGFuZ2UgdG
hvc2UuIiwiY3JlYXRlZCI6MTU0Mzg4MjAxMzgzMH0sIm9FOUlB
TmxJUTVNWnZoQWUiOnsiZGlzY3Vzc2lvbklkIjoiZldlb2l3em
VoRWVSNUNTcSIsInN1YiI6ImdoOjEwMzk0ODk2IiwidGV4dCI6
IlNob3VsZCB3ZSBjaXRlIEJBU0lDIG5vdGF0aW9uPyBJIGZvdW
5kIGl0IG9uIFdpa2lwZWRpYSxcbmh0dHBzOi8vZW4ud2lraXBl
ZGlhLm9yZy93aWtpL0NhbGN1bGF0b3JfaW5wdXRfbWV0aG9kcy
NCQVNJQ19ub3RhdGlvbiIsImNyZWF0ZWQiOjE1NDM4OTczMzM3
OTN9LCJFdU9VdmJGaUg1cVRuS1EwIjp7ImRpc2N1c3Npb25JZC
I6InZBaUExS2dBQm1rWU9jTWUiLCJzdWIiOiJnaDoxMDM5NDg5
NiIsInRleHQiOiJTaG91bGQgd2UgY2l0ZSBCQVNJQyBub3RhdG
lvbj8gSSBmb3VuZCBpdCBvbiBXaWtpcGVkaWEsICBcbltodHRw
czovL2VuLndpa2lwZWRpYS5vcmcvd2lraS9DYWxjdWxhdG9yX2
lucHV0X21ldGhvZHMjQkFTSUNfbm90YXRpb25dKGh0dHBzOi8v
ZW4ud2lraXBlZGlhLm9yZy93aWtpL0NhbGN1bGF0b3JfaW5wdX
RfbWV0aG9kcyNCQVNJQ19ub3RhdGlvbikiLCJjcmVhdGVkIjox
NTQzOTUzNzU0NjQ5fX0sImhpc3RvcnkiOlsxODQyMzcyMDY5LC
0yMjkxMzU3NjksLTExMjMzOTIwNTQsLTg4NzMwMTgyLDIxMDE5
MjQ2ODUsNjAyMDc5NzgwLDEwODUzMDczODIsLTE0NTE3Nzk0Mj
MsLTEwMDk5NTgwMjcsNDg0MjQ4MjE4LDExMzIyMjM4OTMsLTU2
MDM4NzI1NSwtMzMyNjIxNzA2LDE2ODI1MzA0OTMsLTE0OTI5MD
k1Nyw0MjM2NjAxMSwtMjU2OTY1ODM3LC0xMjAxOTEwNDUyLDIw
OTg3NzU5NjBdfQ==
-->