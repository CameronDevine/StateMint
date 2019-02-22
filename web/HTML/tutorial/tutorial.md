# System Dynamics Tutorial

The purpose of this tutorial is to give the necessary background information on how to use the StateMint software to those who have some experience with system dynamics but may need a refresher, or are not familiar with the linear graph method.
To learn more about this subject consider reading _System Dynamics: An Introduction_ by Rowell and Wormley.
Also available are course [notes](http://ricopic.one/dynamic_systems/) for a class at St. Martin's university taught by Prof. Rico Picone, along with [recorded](https://www.youtube.com/watch?v=Fd1C-abrpmg&index=22&list=PLtuwVtW88fOcFdJ9xOBn0T5ta_XPMKHKz) lectures.

## Background Information

This method of finding a differential equation of a dynamic system works with multiple energy domains and any combination of these domains.

### System Types

In each energy domain, a through-variable, $v$, and an across-variable, $f$, is defined.
A through-variable is a variable that generally has the same value at each element terminal.
It corresponds to a physical quantity that would be measured flowing through an element.
An across-variable is a variable that generally has a different value at each element terminal.
It corresponds to a physical quantity that would be measured across an element or relative to some reference.
A list of common system types and their through-variables and across-variables can be found below.

| System Type   | Across-variables              | Through-variables      |
| ------------- | ----------------------------- | ---------------------- |
| Translational | Velocity, $v$                 | Force, $F$             |
| Rotational    | Angular Velocity, $\Omega$    | Torque, $\tau$         |
| Electrical    | Voltage, $v$                  | Current, $i$           |
| Fluid         | Pressure, $P$                 | Flow Rate, $Q$         |
| Thermal       | Temperature Differential, $T$ | Heat Flow Rate, $q$    |

### Elemental Equations

Within each energy domain, there are multiple element types which can be used to model a system in that domain.
Across energy domains, these elements can be grouped into three distinct types.

#### A Type Elements

A type elements are energy storage elements which relate the rate of change of the across-variable to the through-variable of the element.

| System Type   | Element             | Elemental Equation         | Parameter
| ------------- | ------------------- | -------------------------- | ---------
| Translational | Mass                | $F=m\frac{dv}{dt}$         | Mass, $m$
| Rotational    | Inertia             | $\tau=J\frac{d\Omega}{dt}$ | Rotational Inertia, $J$
| Electrical    | Capacitor           | $i=C\frac{dv}{dt}$         | Capacitance, $C$
| Fluid         | Fluid Capacitor     | $Q=C_f\frac{dP}{dt}$       | Fluid Capacitance, $C_f$
| Thermal       | Thermal Capacitance | $q=C_t\frac{dT}{dt}$       | Thermal Capacitance, $C_t$

#### T Type Elements

T type elements are energy storage elements which relate the rate of change of the through-variable to the across-variable of the element.

| System Type   | Element          | Elemental Equation                     | Parameter
| ------------- | ---------------- | -------------------------------------- | ---------
| Translational | Spring           | $v=\frac{1}{K}\frac{dF}{dt}$           | Spring Constant, $K$
| Rotational    | Torsional Spring | $\Omega=\frac{1}{k_r}\frac{d\tau}{dt}$ | Torsional Sprint Constant, $k_r$
| Electrical    | Inductor         | $v=L\frac{di}{dt}$                     | Inductance, $L$
| Fluid         | Inertance        | $P=I_f\frac{dQ}{dt}$                   | Fluid Inertance, $I_f$

#### D Type Elements

D type elements are strictly dissipative with a linear relationship between through-variables and across-variables.

| System Type   | Element            | Elemental Equation         | Parameter
| ------------- | ------------------ | -------------------------- | ---------
| Translational | Damper             | $v=\frac{1}{B}F$           | Viscous Damping Constant, $B$
| Rotational    | Rotational Damper  | $\Omega=\frac{1}{B_r}\tau$ | Rotational Viscous Damping Constant, $B_r$
| Electrical    | Resistor           | $v=Ri$                     | Resistance, $R$
| Fluid         | Fluid Resistance   | $P=R_fQ$                   | Fluid Resistance, $R_f$
| Thermal       | Thermal Resistance | $T=R_tq$                   | Thermal Resistance, $R_t$

#### Transformers

In dynamic systems, energy can flow between multiple domains.
Transformers are one model for relating the through-variable and across-variable of two energy domains to each other,

$\left[\begin{array}{c}v_1\\f_1\end{array}\right]=\left[\begin{array}{cc}TF&0\\0&-1/TF\end{array}\right]\left[\begin{array}{c}v_2\\f_2\end{array}\right]$

Here $TF$ can be used in many different applications.
A few of these are listed below,

| Element                | $TF$       | Parameter
| ---------------------- | ---------- | ---------
| Rack & Pinion          | $r$        | Pinion Pitch Diameter, $r$
| Gear train             | $-r_2/r_1$ | Gear Pitch Diameters, $r_1$ and $r_2$
| DC Motor               | $1/Kv$     | Motor Velocity Constant $Kv$
| Lever                  | $-l_1/l_2$ | Distance to Fulcrum, $l_1$ and $l_2$
| Belt Drive             | $r_2/r_1$  | Pulley Pitch Diameters, $r_1$ and $r_2$
| Electrical transformer | $N_1/N_2$  | Primary Coil Turns, $N_1$ and Secondary Coil Turns, $N_2$
| Fluid Transformer      | $A_2/A_1$  | Fluid Transformer Areas, $A_1$ and $A_2$

#### Gyrators

Gyrators are another tool used to model energy flow between domains.
This model relates the across-variable in one energy domain to the through-variable in the other,

$\left[\begin{array}{c}v_1\\f_1\end{array}\right]=\left[\begin{array}{cc}0&GY\\-1/GY&0\end{array}\right]\left[\begin{array}{c}v_2\\f_2\end{array}\right]$

The following elements can be modeled as gyrators,

| Element           | $GY$   | Parameter
| ----------------- | ------ | ---------
| Hydraulic Ram     | $-1/A$ | Piston Area, $A$
| Displacement Pump | $-1/D$ | Pump Displacement, $D$

#### Sources

The final type of element are the source elements.
Source elements come in two types, across-variable sources and through-variable sources.
These sources allow power to be injected into the system at a given across or through-variable time dependent level.

### Linear Graphs

Linear graph representations of systems use "nodes" and connecting "branches" to diagram a system.
Each node represents an independent across-variable value and is drawn as a dot, or a small circle.
Branches are created for each element in the system, where power flows between the nodes.
Branches are drawn as a line between two nodes with an arrow in the direction of the decreasing across-variable.
In non-electrical systems, A type elements always connect to a ground node.
Arrows on branches point in the direction of decreasing across-variable.
Arrows on transformers and gyrators always point towards ground.
An example of a linear graph appears in the Example section of this tutorial.

### Normal Trees

In order to find the primary and secondary variables, a normal tree can be constructed.
This normal tree should consist of $N-1$ branches from the linear graph where $N$ is the number of nodes in the linear graph.
If multiple ground nodes are present in the linear graph, they should be counted as a single node.
Since the normal tree must be a tree structure, no loops may be created when constructing the normal tree.
To construct the normal tree, select branches in the following order.

1. Across-variable sources
2. A type elements
3. Transformers and Gyrators (minimizing the number of T type elements in the normal tree)
4. D type elements
5. T type elements

For transformers, one branch must be selected.
For gyrators, both or neither branches can be selected.
The elements in the normal tree are termed normal tree branches, while the elements not in the normal tree are called normal tree links.

### Primary and Secondary Variables

Once the normal tree has been created it is trivial to determine the primary and secondary variables.
Primary variables are defined as,

* Across-variables on normal tree branches and
* Through-variables on normal tree links.

For each element, the secondary variable is the non-primary variable.
In other words the secondary variables are,

* Across-variables on normal tree links
* Through-variables on normal tree branches

### State Variables

The state variables of the system are,

* A type elements on normal tree branches and
* T type elements on normal tree links.

### Elemental Equations

We define $B$ as the number of branches in the linear graph and $S$ as the number of sources.
$B-S$ elemental equations should be written with the primary variable on the left hand side.

### Continuity Equations

$N-1-S_A$ continuity equations should be found by drawing a contour around any number of nodes which cuts through exactly one passive (non source) normal tree branch.
For each equation the secondary through-variable should be placed on the left hand side, and the sum of the through-variable flowing through the contour determined.

### Compatibility Equations

$B-N+1-S_T$ compatibility equations should be written with the secondary across-variable on the left side.
To create these equations calculate the sum of the across-variables around the loop created when a normal tree link is added to the normal tree.
Do this for each normal tree link.

## Example

To show how this process works, we will work through the following example.

![Example System](tutorial/tutorial1.svg)

This system is a voltage source which drives a motor with the given resistance and inductance.
This motor in turn drives a pump through a drive shaft with the given stiffness.
Finally the pump pushes water through a curved pipe of known resistance.

### Linear Graph

This system can be distilled into the linear graph below.

![Linear Graph](tutorial/tutorial2.svg)

### Normal Tree

To create the normal tree, first the voltage source is selected.

![Normal Tree](tutorial/tutorial3.svg)

To avoid selecting T type elements (the torsional spring and inductor), The right side of the transformer will be added to the normal tree.

![Normal Tree](tutorial/tutorial4.svg)

Also adding both sides of the gyrator means that adding the torsional spring would cause a loop to be created.

![Normal Tree](tutorial/tutorial6.svg)

Next, the motor resistance is added.

![Normal Tree](tutorial/tutorial7.svg)

Finally to complete the normal tree the motor inductance must be added.

![Normal Tree](tutorial/tutorial8.svg)

### Primary Variables

The following are primary variables determined using the logic above.

$V_s$,
$v_R$,
$v_L$,
$i_1$,
$\Omega_2$,
$\tau_k$,
$\Omega_3$,
$P_4$,
$Q_R$

### Secondary Variables

Given the primary variables above, the following are easily determined to be secondary variables.

$i_s$,
$i_R$,
$i_L$,
$v_1$,
$\tau_2$,
$\Omega_k$,
$\tau_3$,
$Q_4$,
$P_R$

### State Variables

From the requirements the following can be found to be the only state variable.

$\tau_k$

### Elemental Equations

Based on the list of elemental equations, the following list of elemental equations can be generated.

* $v_R=Ri_R$
* $v_L=Li_L'$
* $i_1=-K_v\tau_2$
* $\Omega_2=K_vv_1$
* $\tau_k'=k_t\Omega_k$
* $\Omega_3=\frac{Q_4}{-D}$
* $P_4=\frac{\tau_3}{D}$
* $Q_R=\frac{P_R}{R_f}$

### Continuity Equations

To determine the continuity equations, the following contours can be drawn.

![Normal Tree](tutorial/tutorial9.svg)

Using these contours, the equations below were constructed.

* $i_L=i_1$
* $i_R=i_1$
* $\tau_2=-\tau_k$
* $\tau_3=\tau_k$
* $Q_4=Q_R$

### Compatibility Equations

By adding each link into the normal tree the equations below were generated.

* $v_1=V_s-v_R-v_L$
* $\Omega_k=\Omega_2-\Omega_3$
* $P_R=P_4$

## Using the Software

Given these equations, the state equation could be found by hand, or by using one of the following tools.

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
