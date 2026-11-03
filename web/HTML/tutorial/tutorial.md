# System Dynamics Tutorial

The purpose of this tutorial is to give the necessary background information on how to use the StateMint software to those who have some experience with system dynamics but may need a refresher, or are not familiar with the linear graph method.
To learn more about this subject consider reading _System Dynamics: An Introduction_ by Rowell and Wormley, whose chapter 5 StateMint follows.
Also available are the [System Dynamics](https://systems.ricopic.one/) course notes by Prof. Rico Picone of Saint Martin's University, whose notation this tutorial uses, along with [recorded](https://www.youtube.com/watch?v=Fd1C-abrpmg&index=22&list=PLtuwVtW88fOcFdJ9xOBn0T5ta_XPMKHKz) lectures.

### Notation

This tutorial uses the notation of the notes.
The sans-serif $\mathsf{v}$ and $\mathsf{f}$ are a generalized across-variable and through-variable, distinct from a velocity $v$.
Each variable carries its element's name as a subscript: $v_C$ and $i_C$ are the voltage across and the current through a capacitor $C$, and $T_{K_r}$ is the torque in a rotational spring $K_r$.
$T$ is a torque in a rotational system and a temperature in a thermal one.

StateMint reads plain text, so its variable names differ from the mathematics in two ways.

* Names have no subscripts or Greek letters: write $v_C$ as `vC`, $T_J$ as `TJ`, $\Omega_J$ as `WJ`, and $K_r$ as `Kr`. The full rules are under Input Syntax, below.
* A prime marks a time derivative: `vC'` is $dv_C/dt$.

## Background Information

This method of finding the state-space model of a dynamic system works within each energy domain and across any combination of them.

### Energy Domains

In each energy domain, an across-variable, $\mathsf{v}$, and a through-variable, $\mathsf{f}$, are defined.
An _across-variable_ is the difference between its values at the two ends, or nodes, of an element.
It is measured by an instrument connected across the element, as a voltmeter's two probes go on a resistor's two terminals.
A _through-variable_ passes through an element, the same value entering one end and leaving the other.
It is measured by an instrument placed in series with the element, as an ammeter is.
Except in thermal systems, where the heat flow rate is itself a power, the product $\mathsf{f}\mathsf{v}$ is the power flowing into an element.
The across-variables and through-variables of the common energy domains are listed below.

| Energy Domain | Across-variable, $\mathsf{v}$ | Through-variable, $\mathsf{f}$ |
| ------------- | ----------------------------- | ------------------------------ |
| Translational | Velocity, $v$                 | Force, $F$                     |
| Rotational    | Angular velocity, $\Omega$    | Torque, $T$                    |
| Electronic    | Voltage, $v$                  | Current, $i$                   |
| Fluid         | Pressure, $P$                 | Volumetric flow rate, $Q$      |
| Thermal       | Temperature, $T$              | Heat flow rate, $q$            |

### Element Types

Within each energy domain, there are multiple elements which can be used to model a system in that domain.
Across energy domains, the passive one-port elements can be grouped into three distinct types: two that store energy and one that dissipates it.

#### A-Type Elements

_A-type_ elements are energy storage elements which store energy as a function of their across-variable.
Their elemental equations relate the rate of change of the across-variable to the through-variable, $d\mathsf{v}/dt = \mathsf{f}/\mathsf{C}$, for a generalized capacitance $\mathsf{C}$.

| Energy Domain | Element           | Elemental Equation                 | Parameter
| ------------- | ----------------- | ---------------------------------- | ---------
| Translational | Mass              | $\frac{dv}{dt}=\frac{1}{m}F$       | Mass, $m$
| Rotational    | Moment of inertia | $\frac{d\Omega}{dt}=\frac{1}{J}T$  | Moment of inertia, $J$
| Electronic    | Capacitor         | $\frac{dv}{dt}=\frac{1}{C}i$       | Capacitance, $C$
| Fluid         | Fluid capacitor   | $\frac{dP}{dt}=\frac{1}{C_f}Q$     | Fluid capacitance, $C_f$
| Thermal       | Thermal capacitor | $\frac{dT}{dt}=\frac{1}{C_t}q$     | Thermal capacitance, $C_t$

#### T-Type Elements

_T-type_ elements are energy storage elements which store energy as a function of their through-variable.
Their elemental equations relate the rate of change of the through-variable to the across-variable, $d\mathsf{f}/dt = \mathsf{v}/\mathsf{L}$, for a generalized inductance $\mathsf{L}$.
The thermal domain has no T-type element.

| Energy Domain | Element           | Elemental Equation                 | Parameter
| ------------- | ----------------- | ---------------------------------- | ---------
| Translational | Spring            | $\frac{dF}{dt}=Kv$                 | Spring constant, $K$
| Rotational    | Rotational spring | $\frac{dT}{dt}=K_r\Omega$          | Rotational spring constant, $K_r$
| Electronic    | Inductor          | $\frac{di}{dt}=\frac{1}{L}v$       | Inductance, $L$
| Fluid         | Inertance         | $\frac{dQ}{dt}=\frac{1}{I}P$       | Inertance, $I$

#### D-Type Elements

_D-type_ elements relate their through-variable and across-variable algebraically, $\mathsf{v} = \mathsf{R}\mathsf{f}$, for a generalized resistance $\mathsf{R}$.
All but the thermal resistor dissipate energy; the thermal resistor only impedes its flow.

| Energy Domain | Element           | Elemental Equation                 | Parameter
| ------------- | ----------------- | ---------------------------------- | ---------
| Translational | Damper            | $F=Bv$                             | Damping constant, $B$
| Rotational    | Rotational damper | $T=B_r\Omega$                      | Rotary damping constant, $B_r$
| Electronic    | Resistor          | $v=Ri$                             | Resistance, $R$
| Fluid         | Fluid resistor    | $Q=\frac{1}{R_f}P$                 | Fluid resistance, $R_f$
| Thermal       | Thermal resistor  | $q=\frac{1}{R_t}T$                 | Thermal resistance, $R_t$

#### Transformers

In dynamic systems, energy can flow between multiple domains, or change form within one.
Two-port elements model this: each of their two ports has an across-variable and a through-variable, and the power into each port is taken as positive.
An ideal (lossless) two-port element is either a transformer or a gyrator.
A _transformer_ relates the across-variables of its two ports to each other, and likewise their through-variables, through the transformer ratio

$$
TF = \frac{\mathsf{v_1}}{\mathsf{v_2}} = -\frac{\mathsf{f_2}}{\mathsf{f_1}}.
$$

Its two elemental equations are $\mathsf{v_1} = TF\ \mathsf{v_2}$ and $\mathsf{f_1} = -\mathsf{f_2}/TF$, each rearranged as needed so that it is solved for a primary variable (defined below).
A few elements modeled as transformers are listed below.

| Element                | Port 1        | Port 2          | $TF$       | Parameter
| ---------------------- | ------------- | --------------- | ---------- | ---------
| Rack and pinion        | Rack          | Pinion          | $r$        | Pinion pitch radius, $r$
| Gear train             | Gear 1        | Gear 2          | $-r_2/r_1$ | Gear pitch radii, $r_1$ and $r_2$
| DC motor               | Electrical    | Rotational      | $K_v$      | Back-emf constant, $K_v$, equal to the torque constant $K_t$ in SI units
| Lever                  | End 1         | End 2           | $-l_1/l_2$ | Distances from the fulcrum, $l_1$ and $l_2$
| Belt drive             | Pulley 1      | Pulley 2        | $r_2/r_1$  | Pulley pitch radii, $r_1$ and $r_2$
| Electrical transformer | Primary coil  | Secondary coil  | $N_1/N_2$  | Coil turns, $N_1$ and $N_2$
| Fluid transformer      | Piston 1      | Piston 2        | $A_2/A_1$  | Piston areas, $A_1$ and $A_2$

#### Gyrators

A _gyrator_ relates the across-variable of each port to the through-variable of the other, through the gyrator modulus

$$
GY = \frac{\mathsf{v_1}}{\mathsf{f_2}} = -\frac{\mathsf{v_2}}{\mathsf{f_1}}.
$$

Its two elemental equations are $\mathsf{v_1} = GY\ \mathsf{f_2}$ and $\mathsf{v_2} = -GY\ \mathsf{f_1}$, again rearranged as needed.
The following elements can be modeled as gyrators.

| Element           | Port 1                 | Port 2           | $GY$   | Parameter
| ----------------- | ---------------------- | ---------------- | ------ | ---------
| Hydraulic ram     | Piston (translational) | Cylinder (fluid) | $-1/A$ | Piston area, $A$
| Displacement pump | Shaft (rotational)     | Outlet (fluid)   | $-1/D$ | Pump displacement (volume per radian), $D$

The sign of $TF$ or $GY$ depends on the positive direction chosen at each port, so check the signs in these tables against your own linear graph.

#### Sources

The final type of element is the _ideal source_.
Ideal sources provide (potentially arbitrary) external power to a system by prescribing either their across-variable or their through-variable, independent of the system; the system determines the other variable.
The former are called _across-variable sources_ (voltage, velocity, angular velocity, pressure and temperature sources) and the latter _through-variable sources_ (current, force, torque, flow rate and heat flow rate sources).

### Linear Graphs

A _linear graph_ is a diagram of a system that represents its topology with nodes and edges.
Each _node_ is a point with its own across-variable value, such as a wire in a circuit or a point with its own velocity in a mechanical system, and is drawn as a dot.
One node is the _reference node_, or _ground_, against which across-variables are measured.
Each _edge_ represents one energy port of an element: a one-port element or a source is one edge, and a transformer or gyrator is two.
An edge is drawn as a line between two nodes, with an arrow that assigns the signs of its variables.
(Rowell and Wormley call an edge a _branch_; here, as in the notes, a branch is an edge of a normal tree.)

On a passive element's edge, the across-variable drops in the direction of the arrow and the through-variable flows in the direction of the arrow, so $\mathsf{f}\mathsf{v}$ is the power into the element.
Its arrow may be drawn either way: reversing it reverses the signs of both variables.
A source's arrow is the source's own: the variable it prescribes follows the arrow and the other variable runs against it, so $\mathsf{f}\mathsf{v}$ is the power the source supplies.
For mechanical systems, the notes' sign convention draws a coordinate arrow, points the arrow of each spring and damper along the axis against it, so that a positive force is tension, and points each mass's or inertia's arrow toward ground.
A-type elements other than electrical capacitors always connect to a ground node.
The edges of transformers and gyrators are usually drawn toward ground, as they are in the example below.

### Normal Trees

A _tree_ of a linear graph contains all of its nodes and as many of its edges as possible without forming a loop.
It consists of $N-1$ edges, where $N$ is the number of nodes in the linear graph.
If multiple ground nodes are present in the linear graph, as when transformers and gyrators join separate energy domains, they should be counted as a single node.
The edges in the tree are termed _branches_, while the edges not in the tree are called _links_.
A _normal tree_ is a tree whose branches are selected in the following order.

1. Across-variable sources
2. As many A-type elements as possible
3. Transformers and gyrators (minimizing the number of T-type elements in the normal tree)
4. As many D-type elements as possible
5. Only as many T-type elements as are needed to complete the tree

For transformers, exactly one edge must be selected.
For gyrators, either both edges or neither must be selected.
If the across-variable sources cannot all be selected, or a through-variable source is needed to complete the tree, the sources violate compatibility or continuity, and the model is wrong.

### Primary and Secondary Variables

Once the normal tree has been created, it is straightforward to determine the primary and secondary variables.
_Primary variables_ are defined as,

* across-variables on branches and
* through-variables on links.

The _secondary variable_ is the non-primary variable in each edge.
In other words the secondary variables are,

* through-variables on branches and
* across-variables on links.

### State Variables

The _state variables_ of the system are,

* across-variables on A-type branches and
* through-variables on T-type links.

The system order is their number.
An A-type link or a T-type branch is a _dependent energy storage element_: sources and other energy storage elements fix its variables, so it adds no state variable.
StateMint handles dependent energy storage elements, including any derivatives of the inputs they bring into the model.

### Elemental Equations

We define $E$ as the number of edges in the linear graph and $S$ as the number of sources, $S_A$ of them across-variable sources and $S_T$ of them through-variable sources.
An elemental equation should be written for each of the $E-S$ non-source edges in the linear graph, so a transformer or gyrator gets two.
The primary variable must be written on the left hand side of each equation.
For an independent energy storage element, that is the derivative of its state variable: $d\mathsf{v}/dt = \mathsf{f}/\mathsf{C}$ on an A-type branch and $d\mathsf{f}/dt = \mathsf{v}/\mathsf{L}$ on a T-type link.
A D-type branch gets $\mathsf{v} = \mathsf{R}\mathsf{f}$ and a D-type link $\mathsf{f} = \mathsf{v}/\mathsf{R}$.
A dependent element's equation contains a derivative of its secondary variable: $\mathsf{f} = \mathsf{C} d\mathsf{v}/dt$ on an A-type link and $\mathsf{v} = \mathsf{L} d\mathsf{f}/dt$ on a T-type branch.

### Continuity Equations

$N-1-S_A$ _continuity equations_ should be found, one for each passive (non-source) branch.
Each is found by drawing a contour around any number of nodes that crosses that branch and no other branch.
The through-variables flowing into the contour sum to zero: an edge whose arrow points into the contour contributes $+\mathsf{f}$ and one whose arrow points out contributes $-\mathsf{f}$, except that an across-variable source's through-variable flows against its arrow.
The branch's secondary through-variable should be placed on the left hand side of the resulting equation.

### Compatibility Equations

$E-N+1-S_T$ _compatibility equations_ should be written, one for each passive link.
Adding the link to the normal tree closes exactly one loop.
The across-variables around that loop sum to zero: an edge traversed in the direction of its arrow contributes $+\mathsf{v}$ and one traversed against its arrow contributes $-\mathsf{v}$, except that a through-variable source's across-variable drops against its arrow.
The link's secondary across-variable should be placed on the left hand side of the resulting equation.

## Example

To show how this process works, we will work through the following example.

![Example System](tutorial/tutorial1.svg)

This system is a voltage source $V_s$ which drives a DC motor with back-emf constant $K_v$ and winding resistance $R$ and inductance $L$.
This motor in turn drives a displacement pump, with displacement $D$, through a drive shaft with rotational spring constant $K_r$.
Finally the pump pushes water through a curved pipe with fluid resistance $R_f$.
The output is the flow rate through the pipe, $Q_{R_f}$.
(The figures label the shaft's spring constant $k_t$ and the flow rate $Q_R$.)

### Linear Graph

This system can be distilled into the linear graph below.
Here 1 is the electrical input to the motor, and 2 is its rotational output.
Similarly 3 is the rotational input to the pump, and 4 is its fluid output.
The graph has three separate parts, each with its own ground; counting the grounds as a single node, it has $N=7$ nodes and $E=9$ edges, and its one source is an across-variable source, so $S=S_A=1$ and $S_T=0$.
Taking the shaft's coordinate arrow to point from the pump toward the motor, the spring's arrow points against it, as the sign convention requires.

![Linear Graph](tutorial/tutorial2.svg)

### Normal Tree

To create the normal tree, first the voltage source is selected.

![Normal Tree](tutorial/tutorial3.svg)

There are no A-type elements.
Either side of the transformer leaves one T-type element in the normal tree: side 1 would force the rotational spring into it, and side 2 forces the inductor into it.
The right side of the transformer, 2, will be added to the normal tree.

![Normal Tree](tutorial/tutorial4.svg)

Also adding both sides of the gyrator means that adding the rotational spring would cause a loop to be created, so it remains a link.

![Normal Tree](tutorial/tutorial6.svg)

Next, the motor resistance is added; the pipe's resistance would close a loop with 4.

![Normal Tree](tutorial/tutorial7.svg)

Finally to complete the normal tree the motor inductance must be added.

![Normal Tree](tutorial/tutorial8.svg)

The branches are $V_s$, $R$, $L$, 2, 3 and 4, and the links are 1, $K_r$ and $R_f$.
The inductor is a T-type branch, so it is a dependent energy storage element: through the motor, the shaft's torque fixes its current.

### Primary Variables

The following are primary variables determined using the logic above.

$V_s$,
$v_R$,
$v_L$,
$i_1$,
$\Omega_2$,
$T_{K_r}$,
$\Omega_3$,
$P_4$,
$Q_{R_f}$

### Secondary Variables

Given the primary variables above, the following are easily determined to be secondary variables.

$i_s$,
$i_R$,
$i_L$,
$v_1$,
$T_2$,
$\Omega_{K_r}$,
$T_3$,
$Q_4$,
$P_{R_f}$

### State Variables

The rotational spring is the only T-type link and there are no A-type branches, so the only state variable is

$T_{K_r}$

and the system order is 1.

### Elemental Equations

The $E-S=8$ elemental equations, each solved for its primary variable, are below.
The motor's two come from $TF=K_v$ and the pump's two from $GY=-1/D$.

* $v_R=Ri_R$
* $v_L=L\frac{di_L}{dt}$
* $i_1=-\frac{1}{K_v}T_2$
* $\Omega_2=\frac{1}{K_v}v_1$
* $\frac{dT_{K_r}}{dt}=K_r\Omega_{K_r}$
* $\Omega_3=-\frac{1}{D}Q_4$
* $P_4=\frac{1}{D}T_3$
* $Q_{R_f}=\frac{1}{R_f}P_{R_f}$

### Continuity Equations

To determine the $N-1-S_A=5$ continuity equations, the following contours can be drawn.

![Normal Tree](tutorial/tutorial9.svg)

Using these contours, the equations below were constructed.

* $i_L=i_1$
* $i_R=i_1$
* $T_2=-T_{K_r}$
* $T_3=T_{K_r}$
* $Q_4=-Q_{R_f}$

At the pump's outlet node, the arrows of both 4 and the pipe point out of the contour, so $-Q_4-Q_{R_f}=0$.

### Compatibility Equations

By adding each of the $E-N+1-S_T=3$ links into the normal tree, the equations below were generated.

* $v_1=V_s-v_R-v_L$
* $\Omega_{K_r}=\Omega_2-\Omega_3$
* $P_{R_f}=P_4$

## Using the Software

Given the equations derived above, the state equation could be found by hand.
StateMint does this algebra: it eliminates every variable that is neither a state variable nor an input.
It cannot draw the linear graph, choose the normal tree, or catch a sign error in the equations; those steps remain yours.

### Input Syntax

StateMint takes five lists, named here as in the web interface.

1. **Input Variables:** the variables the sources prescribe.
2. **State Variable Elemental Equations:** one for each state variable, solved for the derivative of the state variable, which is written with a prime, e.g. `vm' = Fm/m`.
3. **Other Elemental Equations:** the remaining elemental equations, each solved for its primary variable.
4. **Constraints:** the continuity and compatibility equations, each solved for a secondary variable.
5. **Output Variables:** variables, or expressions in the system's variables such as `FK + FB`.

These rules apply in the web interface and the Python package.

* In the web interface, entries are separated by new lines or by commas. A comma inside parentheses, as in `atan2(y, x)`, does not split an entry. Blank lines and trailing commas are ignored.
* A list may be empty: a system with only energy storage elements has no other elemental equations.
* Each equation has exactly one `=`, with the variable it is solved for on the left.
* Names are letters, digits and underscores, starting with a letter, and are case-sensitive. Python keywords, such as `lambda`, `in` and `is`, and the function names below can't be names, and `t` (time) and `s` (the Laplace variable) are reserved. `I` is an ordinary name, not the imaginary unit, so it can be an inertance or a current.
* Multiplication is written explicitly, as in `R*iR`, and `^` and `**` both mean a power.
* The functions `sqrt`, `exp`, `log`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh`, `abs` (or `Abs`), `sign`, `Min`, `Max`, `floor`, `ceiling`, `re` and `im`, and the constant `pi`, are available, so nonlinear elements can be modeled.

For the example, writing `W` for $\Omega$, the five lists are below.

**Input Variables:**

```
Vs
```

**State Variable Elemental Equations:**

```
TKr' = Kr*WKr
```

**Other Elemental Equations:**

```
vR = R*iR
vL = L*iL'
i1 = -T2/Kv
W2 = v1/Kv
W3 = -Q4/D
P4 = T3/D
QRf = PRf/Rf
```

**Constraints:**

```
iL = i1
iR = i1
T2 = -TKr
T3 = TKr
Q4 = -QRf
v1 = Vs - vR - vL
WKr = W2 - W3
PRf = P4
```

**Output Variables:**

```
QRf
```

### Results

StateMint returns the state and output equations in the form

$$
\dot{x} = Ax + Bu + E\dot{u}
$$

$$
y = Cx + Du + F\dot{u}
$$

where $x$, $u$ and $y$ are the state, input and output vectors.
The matrices $E$ and $F$ weight derivatives of the inputs, which a dependent energy storage element can bring into the model.
They are usually zero, leaving the standard form $\dot{x} = Ax + Bu$ and $y = Cx + Du$.
When $E$ is not zero, the input derivative can be removed from the state equation by the change of state variable $x' = x - Eu$, which gives

$$
\dot{x}' = Ax' + B'u
$$

$$
y = Cx' + D'u + F\dot{u}
$$

with $B' = AE + B$ and $D' = CE + D$ (Rowell and Wormley, section 5.4, and the notes' section on nonstandard state equations); StateMint gives these too.
It also gives the transfer function matrix $H(s)$ and the state and output equations as $\dot{x} = f(x,u)$ and $y = h(x,u)$, the only form that describes a nonlinear system.

For the example, StateMint finds the state equation $\frac{dT_{K_r}}{dt} = AT_{K_r} + BV_s$ with

$$
A = -\frac{K_r(D^2RR_f + K_v^2)}{D^2R_f(K_rL + K_v^2)}, \qquad B = \frac{K_rK_v}{K_rL + K_v^2}
$$

and the output equation $Q_{R_f} = T_{K_r}/(DR_f)$.
$A$ is negative: the system is stable, as a motor turning a pump should be.
The inductor is dependent, but no input derivative appears, so $E$ and $F$ are zero.

### Web Interface

The web interface is by far the easiest method to perform this algebra,
[ricopic.one/statemint](https://ricopic.one/statemint/?open=tutorial); this link opens it with the example's equations entered.
This interface allows the equations to be entered and the result found without the need to install software.
The result can be shown as equations or as LaTeX, MATLAB, Mathematica or Python code.
A system can be saved in the browser, or downloaded as an `.rnd` file and uploaded later.

### Python

The Python implementation of this software can also be used.
Install it with `pip install StateMint`.
Each of the five lists is a Python list of strings:

```python
import StateMint

sol = StateMint.Solve(
    ["Vs"],
    ["TKr' = Kr*WKr"],
    ["vR = R*iR", "vL = L*iL'", "i1 = -T2/Kv", "W2 = v1/Kv",
     "W3 = -Q4/D", "P4 = T3/D", "QRf = PRf/Rf"],
    ["iL = i1", "iR = i1", "T2 = -TKr", "T3 = TKr", "Q4 = -QRf",
     "v1 = Vs - vR - vL", "WKr = W2 - W3", "PRf = P4"],
    ["QRf"])
print(sol.A, sol.B, sol.C, sol.D)
```

The result's matrices `A`, `B`, `C`, `D`, `E`, `F`, `Bp` ($B'$) and `Dp` ($D'$) are SymPy matrices.
An example notebook is also [provided](https://github.com/CameronDevine/StateMint/blob/master/python/Example.ipynb).

### Mathematica

Finally, the Mathematica package can be used.
It takes the equations as Mathematica expressions, as its [README](https://github.com/CameronDevine/StateMint/blob/master/mathematica/README.md) describes.
An example using Mathematica is also [provided](https://github.com/CameronDevine/StateMint/blob/master/mathematica/Example.nb).
