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
5kIjoyMTMyLCJ0ZXh0IjoidXNlZCJ9LCJFVVJPRjRhRjdCQjd0
OERKIjp7InN0YXJ0Ijo0MDM2LCJlbmQiOjQxMjYsInRleHQiOi
JbZG9jdW1lbnRhdGlvbl0oKSJ9LCJmV2VvaXd6ZWhFZVI1Q1Nx
Ijp7InN0YXJ0IjoyNTMyLCJlbmQiOjI1NDYsInRleHQiOiJCQV
NJQyBub3RhdGlvbiJ9fSwiY29tbWVudHMiOnsiUnlMamsycUxj
cjhEczhKZCI6eyJkaXNjdXNzaW9uSWQiOiJTUjhYckl2em11VW
pGY1paIiwic3ViIjoiZ286MTAyOTA1NDM1NTMwODk2NDc0ODAw
IiwidGV4dCI6IkknbSBhIGJpZyBiZWxpZXZlciB0aGF0IHlvdX
IgZmlyc3Qgc2VudGVuY2Ugc2hvdWxkIHRyeSB0byBjb252ZXkg
dGhlIG1haW4gcG9pbnQgb2YgeW91ciBwYXBlci4gVGhpcyBpcy
Btb3JlIG9mIGFuIFwiaW50cm9kdWN0aW9uXCIgc2VjdGlvbiBz
ZW50ZW5jZSwgYXMgYXJlIHRob3NlIHRoYXQgZm9sbG93IGl0Li
BQZXJoYXBzIHRoaXMgKmlzKiBlZmZlY3RpdmVseSB0aGUgaW50
cm9kdWN0aW9uIGFuZCB0aGVyZSdzIGEgc2VwYXJhdGUgYWJzdH
JhY3QgLi4uIGlmIHNvLCB0aGF0J3MgZmluZS4iLCJjcmVhdGVk
IjoxNTQzNzE5MTAyODMwfSwiemRod2NNWmllRFdySXBrQyI6ey
JkaXNjdXNzaW9uSWQiOiJTUjhYckl2em11VWpGY1paIiwic3Vi
IjoiZ286MTAyOTA1NDM1NTMwODk2NDc0ODAwIiwidGV4dCI6Ik
knbSBnb2luZyB0byBjb250aW51ZSBjb21tZW50aW5nIGFzIGlm
IHRoaXMgdGV4dCBpcyBwcmVjZWRlZCBieSBhbiBhYnN0cmFjdC
BvZiBzb21lIHNvcnQuIiwiY3JlYXRlZCI6MTU0MzcxOTIwMTgw
OH0sInViZHFOaFdTbXRHVWtTV2UiOnsiZGlzY3Vzc2lvbklkIj
oiZXlQd1N4RktaUzd1YmlsbiIsInN1YiI6ImdvOjEwMjkwNTQz
NTUzMDg5NjQ3NDgwMCIsInRleHQiOiJJIHRoaW5rIGFkZGluZy
BhIHBocmFzZSB0byB0aGUgcHJlY2VkaW5nIHNlbnRlbmNlIGNv
dWxkIGNhcHR1cmUgd2hhdCB5b3UncmUgdHJ5aW5nIHRvIHNheS
wgaGVyZS4gU29tZXRoaW5nIGxpa2UgXCIuLi4gbWFrZSBtaXN0
YWtlcywgd2hpY2ggbGVhZCB0byBmcnVzdHJhdGlvbiBhbmQgZG
lzY291cmFnZW1lbnQgd2hlbiBtYW51YWxseSByZWR1Y2luZyB0
aGUgc3lzdGVtIG9mIGVxdWF0aW9ucy5cIiIsImNyZWF0ZWQiOj
E1NDM3MTk2MTA2ODd9LCI0QnJjTmpzRGx4U2JMbE02Ijp7ImRp
c2N1c3Npb25JZCI6ImtJdEwxUVZCSEl5a21UQnQiLCJzdWIiOi
JnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZXh0IjoiV2Ug
Y2FuIG5vdyBiZSBtb3JlIHNwZWNpZmljLCBoZXJlLiBXZSBoYX
ZlIGFscmVhZHkgaW50cm9kdWNlZCB0aGUgZXF1YXRpb25zIGFu
ZCB0aGUgdGFzayBvZiBhdXRvbWF0aW9uLiIsImNyZWF0ZWQiOj
E1NDM3MjAwNjM2OTJ9LCJKcm1kQ3FySUhQVzZuUWNVIjp7ImRp
c2N1c3Npb25JZCI6Ikg1QVdleGFDOHpsWGIyMU8iLCJzdWIiOi
JnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAiLCJ0ZXh0IjoiQ29u
c2lkZXIgZ2V0dGluZyByaWQgb2YgdGhlIGV4aXN0ZW5jZSBzdG
F0ZW1lbnQgYW5kIGluc3RlYWQgZm9jdXMgb24gdGhlIGZhY3Qg
dGhhdCB3ZSAqYXBwbGllZCBleGlzdGluZyogc3ltYm9saWMgbW
F0aCBsaWJyYXJpZXMuIEFsc28gY29uc2lkZXIgY2FsbGluZyBp
dCBcIm1hdGhlbWF0aWNzXCIgYmVjYXVzZSB3ZSdyZSBmYW5jeS
IsImNyZWF0ZWQiOjE1NDM3MjAyNzU2NTl9LCJKNkc2bzg0Y0h0
V0E1dFpQIjp7ImRpc2N1c3Npb25JZCI6IndFRzZWdzhrUXdacG
hXNjMiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4OTY0NzQ4MDAi
LCJ0ZXh0IjoiQ29uc2lkZXIgcmVwaHJhc2luZyB0byBhdm9pZC
BcImRvbmVcIiIsImNyZWF0ZWQiOjE1NDM3MjAzMDQ5MzF9LCJ0
d1pmeUZ4SFZrNGZ2aW1EIjp7ImRpc2N1c3Npb25JZCI6IlF3TE
R2M0gzQk1QTFVMNTAiLCJzdWIiOiJnbzoxMDI5MDU0MzU1MzA4
OTY0NzQ4MDAiLCJ0ZXh0IjoiSSB0aGluayBwcmVzZW50IHRlbn
NlIGlzIGJldHRlciBzaW5jZSB3ZSdyZSBzdGlsbCByZWxlYXNp
bmcgYSBNTUEgcGFja2FnZSIsImNyZWF0ZWQiOjE1NDM3MjAzMz
M1NDh9LCJrblpJUnlsN1JyRVhVVDM2Ijp7ImRpc2N1c3Npb25J
ZCI6InBSS1Rpbm9LZ3NXN1Z0MkgiLCJzdWIiOiJnbzoxMDI5MD
U0MzU1MzA4OTY0NzQ4MDAiLCJ0ZXh0IjoiSSB0aGluayBwZXJo
YXBzIHRoZSBtb3N0IGltcG9ydGFudCBhc3BlY3QgaXMgdGhhdC
BpdCByZXF1aXJlcyBzdHVkZW50cyB0byBsZWFybiBhIG5ldyBz
b2Z0d2FyZSBzeXN0ZW0gLi4uIHdoaWNoIG1vcmUgdGhhbiBvdX
R3ZWlnaHMgdGhlIGFkdmFudGFnZXMgZm9yIG1vc3Qgb2YgdGhl
IHN0dWRlbnRzIC4uLiB5b3VyIHdlYiBhcHAgbGV0cyB0aGVtIG
dldCBzdGFydGVkIHdpdGhvdXQgbGVhcm5pbmcgTU1BIiwiY3Jl
YXRlZCI6MTU0MzcyMDQ0NTY3OH0sIjRveHJSc2hGSWljTTJFT0
8iOnsiZGlzY3Vzc2lvbklkIjoicngyTHVtZGNLVkVpMmZVSyIs
InN1YiI6ImdvOjEwMjkwNTQzNTUzMDg5NjQ3NDgwMCIsInRleH
QiOiJJdCdzIGJlc3QgdG8gYXZvaWQgXCJ1c2VkXCIgLi4uIGFu
ZCBldmVuIGJldHRlciB0byBhdm9pZCB0aGUgcGhyYXNpbmcgdG
hhdCBsZWFkIHRvIGl0LiBFLmcuIHRoaXMgc2VudGVuY2UgY291
bGQgYmUgXCJGb3IgdGhlc2UgcmVhc29ucywgYSB2ZXJzaW9uIG
9mIHRoZSBzb2Z0d2FyZSB3cml0dGVuIGluIHRoZSBQeXRob24g
Li4uLlwiIiwiY3JlYXRlZCI6MTU0MzcyMDY2NTkwNn0sIkV1aU
RhWGs5blhlZW1HalIiOnsiZGlzY3Vzc2lvbklkIjoiRVVST0Y0
YUY3QkI3dDhESiIsInN1YiI6ImdvOjEwMjkwNTQzNTUzMDg5Nj
Q3NDgwMCIsInRleHQiOiJJJ20gYWZyYWlkIHRvIGhhcmRjb2Rl
IHRoZSB1cmwsIGVzcGVjaWFsbHkgaWYgd2UncmUgY2hhbmdpbm
cgdG8gU3RhdGVNaW50IC4uLiIsImNyZWF0ZWQiOjE1NDM3NzY4
MjAyMTV9LCI2Qk40YzVtd3JVaUZnYkVCIjp7ImRpc2N1c3Npb2
5JZCI6IkVVUk9GNGFGN0JCN3Q4REoiLCJzdWIiOiJnaDoxMDM5
NDg5NiIsInRleHQiOiJXaGVuIEkgY2hhbmdlZCB0aGUgbmFtZS
BsYXN0IHRpbWUgSSBkaWQgYSB0ZXh0IHNlYXJjaCBpbiBhbGwg
ZmlsZXMgZm9yIFN0YXRlTW9kZWxSbkQuIFdoZW4gSSBjaGFuZ2
UgdG8gU3RhdGVNaW50IEkgY2FuIHNpbXBseSBzZWFyY2ggZm9y
IGFueSBmaWxlcyB3aGljaCBpbmNsdWRlIGVpdGhlciBTdGF0ZU
1vZGVsUm5EIG9yIFN0YXR1bSBhbmQgY2hhbmdlIHRob3NlLiIs
ImNyZWF0ZWQiOjE1NDM4ODIwMTM4MzB9LCJvRTlJQU5sSVE1TV
p2aEFlIjp7ImRpc2N1c3Npb25JZCI6ImZXZW9pd3plaEVlUjVD
U3EiLCJzdWIiOiJnaDoxMDM5NDg5NiIsInRleHQiOiJTaG91bG
Qgd2UgY2l0ZSBCQVNJQyBub3RhdGlvbj8gSSBmb3VuZCBpdCBv
biBXaWtpcGVkaWEsXG5odHRwczovL2VuLndpa2lwZWRpYS5vcm
cvd2lraS9DYWxjdWxhdG9yX2lucHV0X21ldGhvZHMjQkFTSUNf
bm90YXRpb24iLCJjcmVhdGVkIjoxNTQzODk3MzMzNzkzfX0sIm
hpc3RvcnkiOlsyMTAxOTI0Njg1LDYwMjA3OTc4MCwxMDg1MzA3
MzgyLC0xNDUxNzc5NDIzLC0xMDA5OTU4MDI3LDQ4NDI0ODIxOC
wxMTMyMjIzODkzLC01NjAzODcyNTUsLTMzMjYyMTcwNiwxNjgy
NTMwNDkzLC0xNDkyOTA5NTcsNDIzNjYwMTEsLTI1Njk2NTgzNy
wtMTIwMTkxMDQ1MiwyMDk4Nzc1OTYwXX0=
-->