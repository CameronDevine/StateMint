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
The excellent Python symbolic mathematics library, SymPy [@meurer2017], was instrumental in this implementation.
This code is run as an Amazon AWS Lambda function to allow 
The Python implementation also allows this code to be run as an Amazon AWS Lambda function.

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
xpY2FsbHnigKYifSwiRVVST0Y0YUY3QkI3dDhESiI6eyJzdGFy
dCI6MzkzMSwiZW5kIjo0MDIxLCJ0ZXh0IjoiW2RvY3VtZW50YX
Rpb25dKCkifSwidkFpQTFLZ0FCbWtZT2NNZSI6eyJzdGFydCI6
MjEwOSwiZW5kIjoyMTIzLCJ0ZXh0IjoiQkFTSUMgbm90YXRpb2
4ifX0sImNvbW1lbnRzIjp7IlJ5TGprMnFMY3I4RHM4SmQiOnsi
ZGlzY3Vzc2lvbklkIjoiU1I4WHJJdnptdVVqRmNaWiIsInN1Yi
I6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOiJJ
J20gYSBiaWcgYmVsaWV2ZXIgdGhhdCB5b3VyIGZpcnN0IHNlbn
RlbmNlIHNob3VsZCB0cnkgdG8gY29udmV5IHRoZSBtYWluIHBv
aW50IG9mIHlvdXIgcGFwZXIuIFRoaXMgaXMgbW9yZSBvZiBhbi
BcImludHJvZHVjdGlvblwiIHNlY3Rpb24gc2VudGVuY2UsIGFz
IGFyZSB0aG9zZSB0aGF0IGZvbGxvdyBpdC4gUGVyaGFwcyB0aG
lzICppcyogZWZmZWN0aXZlbHkgdGhlIGludHJvZHVjdGlvbiBh
bmQgdGhlcmUncyBhIHNlcGFyYXRlIGFic3RyYWN0IC4uLiBpZi
BzbywgdGhhdCdzIGZpbmUuIiwiY3JlYXRlZCI6MTU0MzcxOTEw
MjgzMH0sInpkaHdjTVppZURXcklwa0MiOnsiZGlzY3Vzc2lvbk
lkIjoiU1I4WHJJdnptdVVqRmNaWiIsInN1YiI6ImdvOjEwMjkw
NTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOiJJJ20gZ29pbmcgdG
8gY29udGludWUgY29tbWVudGluZyBhcyBpZiB0aGlzIHRleHQg
aXMgcHJlY2VkZWQgYnkgYW4gYWJzdHJhY3Qgb2Ygc29tZSBzb3
J0LiIsImNyZWF0ZWQiOjE1NDM3MTkyMDE4MDh9LCJ1YmRxTmhX
U210R1VrU1dlIjp7ImRpc2N1c3Npb25JZCI6ImV5UHdTeEZLWl
M3dWJpbG4iLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4
MDAiLCJ0ZXh0IjoiSSB0aGluayBhZGRpbmcgYSBwaHJhc2UgdG
8gdGhlIHByZWNlZGluZyBzZW50ZW5jZSBjb3VsZCBjYXB0dXJl
IHdoYXQgeW91J3JlIHRyeWluZyB0byBzYXksIGhlcmUuIFNvbW
V0aGluZyBsaWtlIFwiLi4uIG1ha2UgbWlzdGFrZXMsIHdoaWNo
IGxlYWQgdG8gZnJ1c3RyYXRpb24gYW5kIGRpc2NvdXJhZ2VtZW
50IHdoZW4gbWFudWFsbHkgcmVkdWNpbmcgdGhlIHN5c3RlbSBv
ZiBlcXVhdGlvbnMuXCIiLCJjcmVhdGVkIjoxNTQzNzE5NjEwNj
g3fSwiNEJyY05qc0RseFNiTGxNNiI6eyJkaXNjdXNzaW9uSWQi
OiJrSXRMMVFWQkhJeWttVEJ0Iiwic3ViIjoiZ286MTAyOTA1ND
M1NTMwODk2NDc0ODAwIiwidGV4dCI6IldlIGNhbiBub3cgYmUg
bW9yZSBzcGVjaWZpYywgaGVyZS4gV2UgaGF2ZSBhbHJlYWR5IG
ludHJvZHVjZWQgdGhlIGVxdWF0aW9ucyBhbmQgdGhlIHRhc2sg
b2YgYXV0b21hdGlvbi4iLCJjcmVhdGVkIjoxNTQzNzIwMDYzNj
kyfSwiRXVpRGFYazluWGVlbUdqUiI6eyJkaXNjdXNzaW9uSWQi
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
dGhvc2UuIiwiY3JlYXRlZCI6MTU0Mzg4MjAxMzgzMH0sIkV1T1
V2YkZpSDVxVG5LUTAiOnsiZGlzY3Vzc2lvbklkIjoidkFpQTFL
Z0FCbWtZT2NNZSIsInN1YiI6ImdoOjEwMzk0ODk2IiwidGV4dC
I6IlNob3VsZCB3ZSBjaXRlIEJBU0lDIG5vdGF0aW9uPyBJIGZv
dW5kIGl0IG9uIFdpa2lwZWRpYSwgIFxuW2h0dHBzOi8vZW4ud2
lraXBlZGlhLm9yZy93aWtpL0NhbGN1bGF0b3JfaW5wdXRfbWV0
aG9kcyNCQVNJQ19ub3RhdGlvbl0oaHR0cHM6Ly9lbi53aWtpcG
VkaWEub3JnL3dpa2kvQ2FsY3VsYXRvcl9pbnB1dF9tZXRob2Rz
I0JBU0lDX25vdGF0aW9uKSIsImNyZWF0ZWQiOjE1NDM5NTM3NT
Q2NDl9fSwiaGlzdG9yeSI6Wy02MDU0MTc4MjgsNjcwNDQ3NzEs
LTIyOTEzNTc2OSwtMTEyMzM5MjA1NCwtODg3MzAxODIsMjEwMT
kyNDY4NSw2MDIwNzk3ODAsMTA4NTMwNzM4MiwtMTQ1MTc3OTQy
MywtMTAwOTk1ODAyNyw0ODQyNDgyMTgsMTEzMjIyMzg5MywtNT
YwMzg3MjU1LC0zMzI2MjE3MDYsMTY4MjUzMDQ5MywtMTQ5Mjkw
OTU3LDQyMzY2MDExLC0yNTY5NjU4MzcsLTEyMDE5MTA0NTIsMj
A5ODc3NTk2MF19
-->