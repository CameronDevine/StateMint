# System Dynamics Tutorial

## Purpose

The purpose of this tutorial is to give the necessary background information on how to use the StateMint software to those who have some experience with system dynamics but may need a refresher, or are not familiar with the linear graph method.

## Background Information

This method of finding a differential equation of a dynamic system works with multiple energy domains and any combination of these domains.

### System Types

In each energy domain a through and an across variable is defined.
Through variables are chosen as those whose value remains constant through a given element.
Across variables are those whose value is relative and changes through an element.
A list of system types and their through and across variables can be found below.

| System Type   | Across                   | Through        |
| ------------- | ------------------------ | -------------- |
| Translational | Velocity                 | Force          |
| Rotational    | Angular Velocity         | Torque         |
| Electrical    | Voltage                  | Current        |
| Fluid         | Pressure                 | Flow Rate      |
| Thermal       | Temperature Differential | Heat Flow Rate |

### Elemental Equations

In each energy domain there are multiple different elements which are used to model a system.
Across energy domains these elements can be grouped into three distinct types.

#### A Type Elements

A type elements are energy storage elements which relates the rate of change of the across variable to the through variable of the element.

| System Type   | Element            | Elemental Equation
| ------------- | ------------------ | ------------------
| Translational | Mass               | ![$F=m\frac{dv}{dt}$](http://latex.codecogs.com/svg.latex?F%3Dm%5Cfrac%7Bdv%7D%7Bdt%7D)
| Rotational    | Inertia            | ![$\tau=J\frac{d\Omega}{dt}$](http://latex.codecogs.com/svg.latex?%5Ctau%3DJ%5Cfrac%7Bd%5COmega%7D%7Bdt%7D)
| Electrical    | Capacitor          | ![$i=C\frac{dv}{dt}$](http://latex.codecogs.com/svg.latex?i%3DC%5Cfrac%7Bdv%7D%7Bdt%7D)
| Fluid         | Fluid Capacitor    | ![$Q=C_f\frac{dP}{dt}$](http://latex.codecogs.com/svg.latex?Q%3DC_f%5Cfrac%7BdP%7D%7Bdt%7D)
| Thermal       | Thermal Capacitance | ![$q=C_t\frac{dT}{dt}$](http://latex.codecogs.com/svg.latex?q%3DC_t%5Cfrac%7BdT%7D%7Bdt%7D)

#### T Type Elements

T type elements are energy storage elements which relate the rate of change of the through variable to the across variable of the element.

| System Type   | Element          | Elemental Equation
| ------------- | ---------------- | ------------------
| Translational | Spring           | ![$v=\frac{1}{K}\frac{dF}{dt}$](http://latex.codecogs.com/svg.latex?v%3D%5Cfrac%7B1%7D%7BK%7D%5Cfrac%7BdF%7D%7Bdt%7D)
| Rotational    | Torsional Spring | ![$\Omega=\frac{1}{k_r}\frac{d\tau}{dt}$](http://latex.codecogs.com/svg.latex?%5COmega%3D%5Cfrac%7B1%7D%7Bk_r%7D%5Cfrac%7Bd%5Ctau%7D%7Bdt%7D)
| Electrical    | Inductor         | ![$v=L\frac{di}{dt}$](http://latex.codecogs.com/svg.latex?v%3DL%5Cfrac%7Bdi%7D%7Bdt%7D)
| Fluid         | Inertance        | ![$P=I_f\frac{dQ}{dt}$](http://latex.codecogs.com/svg.latex?P%3DI_f%5Cfrac%7BdQ%7D%7Bdt%7D)

#### D Type Elements

D type elements are strictly dissipative with a linear relationship between through and across variables.

| System Type   | Element            | Elemental Equation
| ------------- | ------------------ | ------------------
| Translational | Damper             | ![$v=\frac{1}{B}F$](http://latex.codecogs.com/svg.latex?v%3D%5Cfrac%7B1%7D%7BB%7DF)
| Rotational    | Rotational Damper  | ![$\Omega=\frac{1}{B_r}\tau$](http://latex.codecogs.com/svg.latex?%5COmega%3D%5Cfrac%7B1%7D%7BB_r%7D%5Ctau)
| Electrical    | Resistor           | ![$v=Ri$](http://latex.codecogs.com/svg.latex?v%3DRi)
| Fluid         | Fluid Resistance   | ![$P=R_fQ$](http://latex.codecogs.com/svg.latex?P%3DR_fQ)
| Thermal       | Thermal Resistance | ![$T=R_tq$](http://latex.codecogs.com/svg.latex?T%3DR_tq)

#### Transformers

In dynamic systems energy can flow between multiple domains.
Transformers are one tool used to model this by relating the through and across variables to each other,

![$\left[\begin{array}{c}v_1\\f_1\end{array}\right]=\left[\begin{array}{cc}TF&0\\0&-1/TF\end{array}\right]\left[\begin{array}{c}v_2\\f_2\end{array}\right]$](http://latex.codecogs.com/svg.latex?%5Cleft%5B%5Cbegin%7Barray%7D%7Bc%7Dv_1%5C%5Cf_1%5Cend%7Barray%7D%5Cright%5D%3D%5Cleft%5B%5Cbegin%7Barray%7D%7Bcc%7DTF%260%5C%5C0%26-1/TF%5Cend%7Barray%7D%5Cright%5D%5Cleft%5B%5Cbegin%7Barray%7D%7Bc%7Dv_2%5C%5Cf_2%5Cend%7Barray%7D%5Cright%5D)

Here ![$TF$](http://latex.codecogs.com/svg.latex?TF) can be used in many different applications.
A few of these are listed below,

| Element                | ![$TF$](http://latex.codecogs.com/svg.latex?TF)
| ---------------------- | ----
| Rack & Pinion          | ![$r$](http://latex.codecogs.com/svg.latex?r)
| Gear train             | ![$-r_2/r_1$](http://latex.codecogs.com/svg.latex?-r_2/r_1)
| DC Motor               | ![$1/Kv$](http://latex.codecogs.com/svg.latex?1/Kv)
| Lever                  | ![$-l_1/l_2$](http://latex.codecogs.com/svg.latex?-l_1/l_2)
| Belt Drive             | ![$r_2/r_1$](http://latex.codecogs.com/svg.latex?r_2/r_1)
| Electrical transformer | ![$N_1/N_2$](http://latex.codecogs.com/svg.latex?N_1/N_2)
| Fluid Transformer      | ![$A_2/A_1$](http://latex.codecogs.com/svg.latex?A_2/A_1)

#### Gyrators

Gyrators are another tool used to model energy flow between domains.
This model relates across variables in one domain to through variables in the other,

![$\left[\begin{array}{c}v_1\\f_1\end{array}\right]=\left[\begin{array}{cc}0&GY\\-1/GY&0\end{array}\right]\left[\begin{array}{c}v_2\\f_2\end{array}\right]$](http://latex.codecogs.com/svg.latex?%5Cleft%5B%5Cbegin%7Barray%7D%7Bc%7Dv_1%5C%5Cf_1%5Cend%7Barray%7D%5Cright%5D%3D%5Cleft%5B%5Cbegin%7Barray%7D%7Bcc%7D0%26GY%5C%5C-1/GY%260%5Cend%7Barray%7D%5Cright%5D%5Cleft%5B%5Cbegin%7Barray%7D%7Bc%7Dv_2%5C%5Cf_2%5Cend%7Barray%7D%5Cright%5D)

The following elements can be modeled as gyrators,

| Element           | ![$GY$](http://latex.codecogs.com/svg.latex?GY)
| ----------------- | ----
| Hydraulic Ram     | ![$-1/A$](http://latex.codecogs.com/svg.latex?-1/A)
| Displacement Pump | ![$-1/D$](http://latex.codecogs.com/svg.latex?-1/D)

### Linear Graph

Linear graph representations of systems use "nodes" and connecting "branches" to diagram a system.
Each node represents an independent across variable value.
Branches are created for each element in the system.
In non electrical systems A type elements always connect to a ground node.
Arrows on branches point in the direction of decreasing across variable.
Arrows on transformers and gyrators always point towards ground.
An example of a linear graph appears in the Example section of this tutorial.

### Normal Tree

In order to find the primary and secondary variables a normal tree can be constructed.
This normal tree should consist of ![$N-1$](http://latex.codecogs.com/svg.latex?N-1) branches from the linear graph where ![$N$](http://latex.codecogs.com/svg.latex?N) is the number of nodes in the linear graph.
If multiple ground nodes are present in the linear graph they should be counted as a single node.
Since the normal tree must be a tree structure no loops may be created when constructing the normal tree.
To construct the normal tree select branches in the following order.

1. Across variable sources
2. A type elements
3. Transformers and Gyrators (minimizing the number of T type elements in the normal tree)
4. D type elements
5. T type elements

For transformers one branch must be selected, and for gyrators both or neither branches can be selected.
The elements in the normal tree are termed normal tree branches, while the elements not in the normal tree are called normal tree links.

### Primary Variables

Once the normal tree has been created it is trivial to determine the primary and secondary variables. These are defined as,

* Across variables on normal tree branches
* Through variables on normal tree links

For each element the secondary variable is the non primary variable. In other words the secondary variables are,

* Across variables on normal tree links
* Through variables on normal tree branches

### State Variables

The state variables of the system are,

* A type elements on normal tree branches
* T type elements on normal tree links

### Elemental Equations

![$B-S$](http://latex.codecogs.com/svg.latex?B-S) elemental equations should be written with the primary variable on the left hand side.
Here ![$B$](http://latex.codecogs.com/svg.latex?B) is the number of branches in the linear graph and ![$S$](http://latex.codecogs.com/svg.latex?S) is the number of sources.

### Continuity Equations

![$N-1-S_A$](http://latex.codecogs.com/svg.latex?N-1-S_A) continuity equations should be found by drawing a contour around any number of nodes which cuts through exactly one passive (non source) normal tree branch.
For each equation the secondary through variable should be placed on the left hand side, and the sum of the through variable flowing through the contour determined.

### Compatibility Equations

![$B-N+1-S_T$](http://latex.codecogs.com/svg.latex?B-N%2B1-S_T) compatibility equations should be written with the secondary across variable on the left side.
To create these equations calculate the sum of the across variables around the loop created when a normal tree link is added to the normal tree.
Do this for each normal tree link.

## Example

To show how this process works, we will work through the following example.

![Example System](web/HTML/tutorial/tutorial1.svg)

This system is a voltage source which drives a motor with the given resistance and inductance.
This motor in turn drives a pump through a drive shaft with the given stiffness.
Finally the pump pushes water through a curved pipe of known resistance.

### Linear Graph

This system can be distilled into the linear graph below.

![Linear Graph](web/HTML/tutorial/tutorial2.svg)

### Normal Tree

To create the normal tree, first the voltage source is selected.

![Normal Tree](web/HTML/tutorial/tutorial3.svg)

To avoid selecting T type elements (the torsional spring and inductor), The right side of the transformer will be added to the normal tree.

![Normal Tree](web/HTML/tutorial/tutorial4.svg)

Also adding both sides of the gyrator means that adding the torsional spring would cause a loop to be created.

![Normal Tree](web/HTML/tutorial/tutorial6.svg)

Next a the motor resistance is added.

![Normal Tree](web/HTML/tutorial/tutorial7.svg)

Finally to complete the normal tree the motor inductance must be added.

![Normal Tree](web/HTML/tutorial/tutorial8.svg)

### Primary Variables

The following are primary variables determined using the logic above.

![$V_s$](http://latex.codecogs.com/svg.latex?V_s),
![$v_R$](http://latex.codecogs.com/svg.latex?v_R),
![$v_L$](http://latex.codecogs.com/svg.latex?v_L),
![$i_1$](http://latex.codecogs.com/svg.latex?i_1),
![$\Omega_2$](http://latex.codecogs.com/svg.latex?%5COmega_2),
![$\tau_k$](http://latex.codecogs.com/svg.latex?%5Ctau_k),
![$\Omega_3$](http://latex.codecogs.com/svg.latex?%5COmega_3),
![$P_4$](http://latex.codecogs.com/svg.latex?P_4),
![$Q_R$](http://latex.codecogs.com/svg.latex?Q_R)

### Secondary Variables

Given the primary variables above the following are easily determined to be secondary variables.

![$i_s$](http://latex.codecogs.com/svg.latex?i_s),
![$i_R$](http://latex.codecogs.com/svg.latex?i_R),
![$i_L$](http://latex.codecogs.com/svg.latex?i_L),
![$v_1$](http://latex.codecogs.com/svg.latex?v_1),
![$\tau_2$](http://latex.codecogs.com/svg.latex?%5Ctau_2),
![$\Omega_k$](http://latex.codecogs.com/svg.latex?%5COmega_k),
![$\tau_3$](http://latex.codecogs.com/svg.latex?%5Ctau_3),
![$Q_4$](http://latex.codecogs.com/svg.latex?Q_4),
![$P_R$](http://latex.codecogs.com/svg.latex?P_R)

### State Variables

From the requirements the following can be found to be the only state variable.

![$\tau_k$](http://latex.codecogs.com/svg.latex?%5Ctau_k)

### Elemental Equations

Based on the list of elemental equations the following list of elemental equations can be generated.

* ![$v_R=Ri_R$](http://latex.codecogs.com/svg.latex?v_R%3DRi_R)
* ![$v_L=Li_L'$](http://latex.codecogs.com/svg.latex?v_L%3DLi_L%27)
* ![$i_1=-K_v\tau_2$](http://latex.codecogs.com/svg.latex?i_1%3D-K_v%5Ctau_2)
* ![$\Omega_2=K_vv_1$](http://latex.codecogs.com/svg.latex?%5COmega_2%3DK_vv_1)
* ![$\tau_k'=k_t\Omega_k$](http://latex.codecogs.com/svg.latex?%5Ctau_k%27%3Dk_t%5COmega_k)
* ![$\Omega_3=\frac{Q_4}{-D}$](http://latex.codecogs.com/svg.latex?%5COmega_3%3D%5Cfrac%7BQ_4%7D%7B-D%7D)
* ![$P_4=\frac{\tau_3}{D}$](http://latex.codecogs.com/svg.latex?P_4%3D%5Cfrac%7B%5Ctau_3%7D%7BD%7D)
* ![$Q_R=\frac{P_R}{R_f}$](http://latex.codecogs.com/svg.latex?Q_R%3D%5Cfrac%7BP_R%7D%7BR_f%7D)

### Continuity Equations

To determine the continuity equations the following contours can be drawn.

![Normal Tree](web/HTML/tutorial/tutorial9.svg)

Using these contours the equations below were constructed.

* ![$i_L=i_1$](http://latex.codecogs.com/svg.latex?i_L%3Di_1)
* ![$i_R=i_1$](http://latex.codecogs.com/svg.latex?i_R%3Di_1)
* ![$\tau_2=-\tau_k$](http://latex.codecogs.com/svg.latex?%5Ctau_2%3D-%5Ctau_k)
* ![$\tau_3=\tau_k$](http://latex.codecogs.com/svg.latex?%5Ctau_3%3D%5Ctau_k)
* ![$Q_4=Q_R$](http://latex.codecogs.com/svg.latex?Q_4%3DQ_R)

### Compatibility Equations

By adding each link into the normal tree the equations below were generated.

* ![$v_1=V_s-v_R-v_L$](http://latex.codecogs.com/svg.latex?v_1%3DV_s-v_R-v_L)
* ![$\Omega_k=\Omega_2-\Omega_3$](http://latex.codecogs.com/svg.latex?%5COmega_k%3D%5COmega_2-%5COmega_3)
* ![$P_R=P_4$](http://latex.codecogs.com/svg.latex?P_R%3DP_4)

## Using the Software

Given these equations the state equation could be found by hand, or one of the following tools could be used.

### Web Interface

The web interface is by far the easiest method to perform this algebra,
[statemint.stmartin.edu](http://statemint.stmartin.edu/?%7B%22InVars%22%3A%22Vs%22%2C%22StVarElEqns%22%3A%22tk'%20%3D%20kt%20*%20wk%22%2C%22OtherElEqns%22%3A%22vR%20%3D%20R%20*%20iR%2C%5CnvL%20%3D%20L%20*%20iL'%2C%5Cni1%20%3D%20-Kv%20*%20t2%2C%5Cnw2%20%3D%20Kv%20*%20v1%2C%5Cnw3%20%3D%20Q4%20%2F%20-D%2C%5CnP4%20%3D%20t3%20%2F%20D%2C%5CnQR%20%3D%20PR%20%2F%20Rf%22%2C%22Constraints%22%3A%22iL%20%3D%20i1%2C%5CniR%20%3D%20i1%2C%5Cnt2%20%3D%20-tk%2C%5Cnt3%20%3D%20tk%2C%5CnQ4%20%3D%20QR%2C%5Cnv1%20%3D%20Vs%20-%20vR%20-%20vL%2C%5Cnwk%20%3D%20w2%20-%20w3%2C%5CnPR%20%3D%20P4%22%2C%22OutputVars%22%3A%22QR%22%7D).
This interface allow the equations to be entered and the result found without the need to install software.

### Python

The Python implementation of this software can also be used.
An example continuing this tutorial is [provided](https://github.com/CameronDevine/StateMint/blob/master/python/Example.ipynb).

### Mathematica

Finally, the Mathematica package can be used.
An example using Mathematica is also [provided](https://github.com/CameronDevine/StateMint/blob/master/mathematica/Example.nb).

## Further reading

To learn more about this subject consider reading _System Dynamics: An Introduction_ by Rowell and Wormley.
Also available are course [notes](http://ricopic.one/dynamic_systems/) for a class at St. Martin's university taught by Prof. Rico Picone, along with [recorded](https://www.youtube.com/watch?v=Fd1C-abrpmg&index=22&list=PLtuwVtW88fOcFdJ9xOBn0T5ta_XPMKHKz) lectures.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEzNTMxOTAxODZdfQ==
-->
