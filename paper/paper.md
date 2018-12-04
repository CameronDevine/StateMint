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
The next step is to algebraically eliminate those variables that are not state or input variables from the equations until a minimal set of differential equations remains.
During this step of manually reducing the system of equations is where students often make mistakes, leading to frustration and discouragement.
However, this algebra is not a necessary component of a strong understanding of system dynamics and can be easily automated using tools we present here.


To aid students in their learning process a program was written to symbolically determine the differential equations using the elemental and constraint equations as input.
This program allows students to focus on the process of creating a dynamic system model without worrying about algebraic mistakes.
This allows the student to focus on course content which is new and unique.

Because symbolic math libraries already exist, writing this software is a relatively trivial task.
This was originally done in Mathematica because of its advanced symbolic math capabilities.
However, this required students to purchase and install Mathematica.
Because of the size and cost of Mathematica a more economical solution was desired.
To solve this problem the Python programming language along with SymPy [@meurer2017], a symbolic math library, was used to recreate the software.
This provides the same functionality without the cost barrier and with a smaller installed size.
The Python implementation also allows this code to be run as an Amazon AWS Lambda function.
With the Lambda function, a website was designed to allow this software to be used with any device which has an internet connection and a web browser.
Because equations are entered in BASIC notation, similar to most scientific calculators, no programming knowledge is needed to use this interface.

# Mathematica Package

The Mathematica package `StateMint` can be installed via the [documentation](https://github.com/CameronDevine/Statum/blob/master/mathematica/README.md). The central function of the package is `stateEquations`, which uses an algorithm similar to that of the Python package, above, to derive the state equations. It takes as arguments lists of elemental equations, constraint equations, primary variables, and input variables and returns the vector state equation, state variables, and the time-derivative of the state variables.

The `outputEquations` function derives the output equations given output expressions in terms of primary and secondary variables (including inputs). The function accepts lists of input variables, state variables, elemental and constraint equations, and output expressions.

The functions `stateEquations` and `outputEquations` yield what are in general *nonlinear* state and output equations. Linear state and output equations are typically written in a standard vector form described by matrices `A`, `B`, `C`, and `D` (and sometimes `E` and `F`). The `linearizeState` function accepts lists of input variables, state variables, and the time-derivatives of the state vector (from `stateEquations`) and returns the `A`, `B`, and `E` matrices. Similarly, `linearizeOutput` returns the `C`, `D`, and `F` matrices.

An example of how to use this package is [included](https://github.com/CameronDevine/Statum/blob/master/mathematica/Example.nb).

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
An automated installer is also [included](https://github.com/CameronDevine/Statum/tree/master/web).

# Acknowledgments

The authors would like to acknowledge the work of [Gavin Basuel](https://www.gavinbasuel.com/) who designed the user experience for the web interface and helped with HTML/CSS development.

# References

<!--stackedit_data:
eyJkaXNjdXNzaW9ucyI6eyJTUjhYckl2em11VWpGY1paIjp7In
N0YXJ0Ijo2NjIsImVuZCI6ODE3LCJ0ZXh0IjoiV2hlbiBkZXRl
cm1pbmluZyB0aGUgZGlmZmVyZW50aWFsIGVxdWF0aW9uIG9mIG
EgZHluYW1pYyBzeXN0ZW0gdXNpbmcgbGluZWFyIGdyYeKApiJ9
LCJleVB3U3hGS1pTN3ViaWxuIjp7InN0YXJ0IjoxMTM0LCJlbm
QiOjExMzQsInRleHQiOiJXaGVuIGxlYXJuaW5nIHN5c3RlbSBk
eW5hbWljcywgc3R1ZGVudHMgd29yayBtYW55IHByb2JsZW1zIG
FzIGEgcGFydCBvZiB0aGVpciBj4oCmIn0sImtJdEwxUVZCSEl5
a21UQnQiOnsic3RhcnQiOjEyODksImVuZCI6MTQ2MCwidGV4dC
I6IlRvIGFpZCBzdHVkZW50cyBpbiB0aGVpciBsZWFybmluZyBw
cm9jZXNzIGEgcHJvZ3JhbSB3YXMgd3JpdHRlbiB0byBzeW1ib2
xpY2FsbHnigKYifSwiSDVBV2V4YUM4emxYYjIxTyI6eyJzdGFy
dCI6MTY2OSwiZW5kIjoxNzY3LCJ0ZXh0IjoiQmVjYXVzZSBzeW
1ib2xpYyBtYXRoIGxpYnJhcmllcyBhbHJlYWR5IGV4aXN0LCB3
cml0aW5nIHRoaXMgc29mdHdhcmUgaXMgYSByZWxhdOKApiJ9LC
J3RUc2Vnc4a1F3WnBoVzYzIjp7InN0YXJ0IjoxNzg4LCJlbmQi
OjE3OTIsInRleHQiOiJkb25lIn0sIlF3TER2M0gzQk1QTFVMNT
AiOnsic3RhcnQiOjE4NzQsImVuZCI6MTg4MiwidGV4dCI6InJl
cXVpcmVkIn0sInBSS1Rpbm9LZ3NXN1Z0MkgiOnsic3RhcnQiOj
E5NDQsImVuZCI6MTk1NywidGV4dCI6InNpemUgYW5kIGNvc3Qi
fSwicngyTHVtZGNLVkVpMmZVSyI6eyJzdGFydCI6MjEyOCwiZW
5kIjoyMTMyLCJ0ZXh0IjoidXNlZCJ9LCJTQ25ucDJUY0FaNmVk
SVRDIjp7InN0YXJ0IjoyNjQ3LCJlbmQiOjI2NjgsInRleHQiOi
IjIE1hdGhlbWF0aWNhIFBhY2thZ2UifSwiRVVST0Y0YUY3QkI3
dDhESiI6eyJzdGFydCI6MjczMSwiZW5kIjoyODIxLCJ0ZXh0Ij
oiW2RvY3VtZW50YXRpb25dKCkifSwiZldlb2l3emVoRWVSNUNT
cSI6eyJzdGFydCI6MjUzMiwiZW5kIjoyNTQ2LCJ0ZXh0IjoiQk
FTSUMgbm90YXRpb24ifX0sImNvbW1lbnRzIjp7IlJ5TGprMnFM
Y3I4RHM4SmQiOnsiZGlzY3Vzc2lvbklkIjoiU1I4WHJJdnptdV
VqRmNaWiIsInN1YiI6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgw
MCIsInRleHQiOiJJJ20gYSBiaWcgYmVsaWV2ZXIgdGhhdCB5b3
VyIGZpcnN0IHNlbnRlbmNlIHNob3VsZCB0cnkgdG8gY29udmV5
IHRoZSBtYWluIHBvaW50IG9mIHlvdXIgcGFwZXIuIFRoaXMgaX
MgbW9yZSBvZiBhbiBcImludHJvZHVjdGlvblwiIHNlY3Rpb24g
c2VudGVuY2UsIGFzIGFyZSB0aG9zZSB0aGF0IGZvbGxvdyBpdC
4gUGVyaGFwcyB0aGlzICppcyogZWZmZWN0aXZlbHkgdGhlIGlu
dHJvZHVjdGlvbiBhbmQgdGhlcmUncyBhIHNlcGFyYXRlIGFic3
RyYWN0IC4uLiBpZiBzbywgdGhhdCdzIGZpbmUuIiwiY3JlYXRl
ZCI6MTU0MzcxOTEwMjgzMH0sInpkaHdjTVppZURXcklwa0MiOn
siZGlzY3Vzc2lvbklkIjoiU1I4WHJJdnptdVVqRmNaWiIsInN1
YiI6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleHQiOi
JJJ20gZ29pbmcgdG8gY29udGludWUgY29tbWVudGluZyBhcyBp
ZiB0aGlzIHRleHQgaXMgcHJlY2VkZWQgYnkgYW4gYWJzdHJhY3
Qgb2Ygc29tZSBzb3J0LiIsImNyZWF0ZWQiOjE1NDM3MTkyMDE4
MDh9LCJ1YmRxTmhXU210R1VrU1dlIjp7ImRpc2N1c3Npb25JZC
I6ImV5UHdTeEZLWlM3dWJpbG4iLCJzdWIiOiJnbzoxMDI5MDU0
MzU1MzA4OTY0NzQ4MDAiLCJ0ZXh0IjoiSSB0aGluayBhZGRpbm
cgYSBwaHJhc2UgdG8gdGhlIHByZWNlZGluZyBzZW50ZW5jZSBj
b3VsZCBjYXB0dXJlIHdoYXQgeW91J3JlIHRyeWluZyB0byBzYX
ksIGhlcmUuIFNvbWV0aGluZyBsaWtlIFwiLi4uIG1ha2UgbWlz
dGFrZXMsIHdoaWNoIGxlYWQgdG8gZnJ1c3RyYXRpb24gYW5kIG
Rpc2NvdXJhZ2VtZW50IHdoZW4gbWFudWFsbHkgcmVkdWNpbmcg
dGhlIHN5c3RlbSBvZiBlcXVhdGlvbnMuXCIiLCJjcmVhdGVkIj
oxNTQzNzE5NjEwNjg3fSwiNEJyY05qc0RseFNiTGxNNiI6eyJk
aXNjdXNzaW9uSWQiOiJrSXRMMVFWQkhJeWttVEJ0Iiwic3ViIj
oiZ286MTAyOTA1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6Ildl
IGNhbiBub3cgYmUgbW9yZSBzcGVjaWZpYywgaGVyZS4gV2UgaG
F2ZSBhbHJlYWR5IGludHJvZHVjZWQgdGhlIGVxdWF0aW9ucyBh
bmQgdGhlIHRhc2sgb2YgYXV0b21hdGlvbi4iLCJjcmVhdGVkIj
oxNTQzNzIwMDYzNjkyfSwiSnJtZENxcklIUFc2blFjVSI6eyJk
aXNjdXNzaW9uSWQiOiJINUFXZXhhQzh6bFhiMjFPIiwic3ViIj
oiZ286MTAyOTA1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6IkNv
bnNpZGVyIGdldHRpbmcgcmlkIG9mIHRoZSBleGlzdGVuY2Ugc3
RhdGVtZW50IGFuZCBpbnN0ZWFkIGZvY3VzIG9uIHRoZSBmYWN0
IHRoYXQgd2UgKmFwcGxpZWQgZXhpc3RpbmcqIHN5bWJvbGljIG
1hdGggbGlicmFyaWVzLiBBbHNvIGNvbnNpZGVyIGNhbGxpbmcg
aXQgXCJtYXRoZW1hdGljc1wiIGJlY2F1c2Ugd2UncmUgZmFuY3
kiLCJjcmVhdGVkIjoxNTQzNzIwMjc1NjU5fSwiSjZHNm84NGNI
dFdBNXRaUCI6eyJkaXNjdXNzaW9uSWQiOiJ3RUc2Vnc4a1F3Wn
BoVzYzIiwic3ViIjoiZ286MTAyOTA1NDM1NTMwODk2NDc0ODAw
IiwidGV4dCI6IkNvbnNpZGVyIHJlcGhyYXNpbmcgdG8gYXZvaW
QgXCJkb25lXCIiLCJjcmVhdGVkIjoxNTQzNzIwMzA0OTMxfSwi
dHdaZnlGeEhWazRmdmltRCI6eyJkaXNjdXNzaW9uSWQiOiJRd0
xEdjNIM0JNUExVTDUwIiwic3ViIjoiZ286MTAyOTA1NDM1NTMw
ODk2NDc0ODAwIiwidGV4dCI6IkkgdGhpbmsgcHJlc2VudCB0ZW
5zZSBpcyBiZXR0ZXIgc2luY2Ugd2UncmUgc3RpbGwgcmVsZWFz
aW5nIGEgTU1BIHBhY2thZ2UiLCJjcmVhdGVkIjoxNTQzNzIwMz
MzNTQ4fSwia25aSVJ5bDdSckVYVVQzNiI6eyJkaXNjdXNzaW9u
SWQiOiJwUktUaW5vS2dzVzdWdDJIIiwic3ViIjoiZ286MTAyOT
A1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6IkkgdGhpbmsgcGVy
aGFwcyB0aGUgbW9zdCBpbXBvcnRhbnQgYXNwZWN0IGlzIHRoYX
QgaXQgcmVxdWlyZXMgc3R1ZGVudHMgdG8gbGVhcm4gYSBuZXcg
c29mdHdhcmUgc3lzdGVtIC4uLiB3aGljaCBtb3JlIHRoYW4gb3
V0d2VpZ2hzIHRoZSBhZHZhbnRhZ2VzIGZvciBtb3N0IG9mIHRo
ZSBzdHVkZW50cyAuLi4geW91ciB3ZWIgYXBwIGxldHMgdGhlbS
BnZXQgc3RhcnRlZCB3aXRob3V0IGxlYXJuaW5nIE1NQSIsImNy
ZWF0ZWQiOjE1NDM3MjA0NDU2Nzh9LCI0b3hyUnNoRklpY00yRU
9PIjp7ImRpc2N1c3Npb25JZCI6InJ4Mkx1bWRjS1ZFaTJmVUsi
LCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZX
h0IjoiSXQncyBiZXN0IHRvIGF2b2lkIFwidXNlZFwiIC4uLiBh
bmQgZXZlbiBiZXR0ZXIgdG8gYXZvaWQgdGhlIHBocmFzaW5nIH
RoYXQgbGVhZCB0byBpdC4gRS5nLiB0aGlzIHNlbnRlbmNlIGNv
dWxkIGJlIFwiRm9yIHRoZXNlIHJlYXNvbnMsIGEgdmVyc2lvbi
BvZiB0aGUgc29mdHdhcmUgd3JpdHRlbiBpbiB0aGUgUHl0aG9u
IC4uLi5cIiIsImNyZWF0ZWQiOjE1NDM3MjA2NjU5MDZ9LCI0Y3
hpQUZmQ2FyU2Y2NXZqIjp7ImRpc2N1c3Npb25JZCI6IlNDbm5w
MlRjQVo2ZWRJVEMiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OT
Y0NzQ4MDAiLCJ0ZXh0IjoiQ29uc2lkZXIgcmVvcmRlcmluZyB0
aGVzZSAuLi4gYXQgbGVhc3QgcHV0dGluZyBNTUEgbGFzdCwgc2
luY2UgSSB0aGluayBpdCdzIGxlYXN0IGltcG9ydGFudC4iLCJj
cmVhdGVkIjoxNTQzNzIyNTMxNjc3fSwiRXVpRGFYazluWGVlbU
dqUiI6eyJkaXNjdXNzaW9uSWQiOiJFVVJPRjRhRjdCQjd0OERK
Iiwic3ViIjoiZ286MTAyOTA1NDM1NTMwODk2NDc0ODAwIiwidG
V4dCI6IkknbSBhZnJhaWQgdG8gaGFyZGNvZGUgdGhlIHVybCwg
ZXNwZWNpYWxseSBpZiB3ZSdyZSBjaGFuZ2luZyB0byBTdGF0ZU
1pbnQgLi4uIiwiY3JlYXRlZCI6MTU0Mzc3NjgyMDIxNX0sIjZC
TjRjNW13clVpRmdiRUIiOnsiZGlzY3Vzc2lvbklkIjoiRVVST0
Y0YUY3QkI3dDhESiIsInN1YiI6ImdoOjEwMzk0ODk2IiwidGV4
dCI6IldoZW4gSSBjaGFuZ2VkIHRoZSBuYW1lIGxhc3QgdGltZS
BJIGRpZCBhIHRleHQgc2VhcmNoIGluIGFsbCBmaWxlcyBmb3Ig
U3RhdGVNb2RlbFJuRC4gV2hlbiBJIGNoYW5nZSB0byBTdGF0ZU
1pbnQgSSBjYW4gc2ltcGx5IHNlYXJjaCBmb3IgYW55IGZpbGVz
IHdoaWNoIGluY2x1ZGUgZWl0aGVyIFN0YXRlTW9kZWxSbkQgb3
IgU3RhdHVtIGFuZCBjaGFuZ2UgdGhvc2UuIiwiY3JlYXRlZCI6
MTU0Mzg4MjAxMzgzMH0sIjhpMmFzRjUzakpGVFlMN3giOnsiZG
lzY3Vzc2lvbklkIjoiU0NubnAyVGNBWjZlZElUQyIsInN1YiI6
ImdoOjEwMzk0ODk2IiwidGV4dCI6IkkgdGhpbmsgSSBvcmlnaW
5hbGx5IG9yZGVyZWQgdGhlIHNlY3Rpb25zIHRoaXMgd2F5IGJl
Y2F1c2UgdGhlIE1hdGhlbWF0aWNhIHZlcnNpb24gd2FzIHdyaX
R0ZW4gZmlyc3QuIEl0IG1ha2VzIHNlbnNlIHRoYXQgdGhlIHZl
cnNpb24gdGhhdCBpcyBtb3N0IGxpa2VseSB0byBiZSB1c2VkIH
Nob3VsZCBiZSBwdXQgZmlyc3QuIFNvIHNob3VsZCBJIGNoYW5n
ZSB0aGUgb3JkZXIgdG8gMS4gV2ViIEludGVyZmFjZSwgMi4gUH
l0aG9uLCBhbmQgMy4gTWF0aGVtYXRpY2E/IiwiY3JlYXRlZCI6
MTU0Mzg4MjE2MzAyM30sIm9FOUlBTmxJUTVNWnZoQWUiOnsiZG
lzY3Vzc2lvbklkIjoiZldlb2l3emVoRWVSNUNTcSIsInN1YiI6
ImdoOjEwMzk0ODk2IiwidGV4dCI6IlNob3VsZCB3ZSBjaXRlIE
JBU0lDIG5vdGF0aW9uPyBJIGZvdW5kIGl0IG9uIFdpa2lwZWRp
YSxcbmh0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy93aWtpL0NhbG
N1bGF0b3JfaW5wdXRfbWV0aG9kcyNCQVNJQ19ub3RhdGlvbiIs
ImNyZWF0ZWQiOjE1NDM4OTczMzM3OTN9fSwiaGlzdG9yeSI6Wz
EwODUzMDczODIsLTE0NTE3Nzk0MjMsLTEwMDk5NTgwMjcsNDg0
MjQ4MjE4LDExMzIyMjM4OTMsLTU2MDM4NzI1NSwtMzMyNjIxNz
A2LDE2ODI1MzA0OTMsLTE0OTI5MDk1Nyw0MjM2NjAxMSwtMjU2
OTY1ODM3LC0xMjAxOTEwNDUyLDIwOTg3NzU5NjBdfQ==
-->