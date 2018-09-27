# System Dynamics Tutorial

## Purpose

The purpose of this tutorial is to give the necessary background information on how to use the StateModelRnD software to those who have some experience with system dynamics but may need a refresher, or are not familiar with the method of Rowell and Wormley.

## Background Information

### System Types

| System Type   | Accross                  | Through        |
| ------------- | ------------------------ | -------------- |
| Translational | Velocity                 | Force          |
| Rotational    | Angular Velocity         | Torque         |
| Electrical    | Voltage                  | Current        |
| Fluid         | Pressure                 | Flow Rate      |
| Thermal       | Temperature Differential | Heat Flow Rate |

### Elemental Equations

#### A Type Elements

| System Type   | Element            | Elemental Equation      |
| ------------- | ------------------ | ----------------------- |
| Translational | Mass               | $F=m\frac{dv}{dt}$      |
| Rotational    | Inertia            | $T=J\frac{d\Omega}{dt}$ |
| Electrical    | Capacitor          | $i=C\frac{dv}{dt}$      |
| Fluid         | Fluid Capacitor    | $Q=C_f\frac{dP}{dt}$    |
| Thermal       | Thermal Capictance | $q=C_t\frac{dT}{dt}$    |

#### T Type Elements

| System Type   | Element          | Elemental Equation                  |
| ------------- | ---------------- | ----------------------------------- |
| Translational | Spring           | $v=\frac{1}{K}\frac{dF}{dt}$        |
| Rotational    | Torsional Spring | $\Omega=\frac{1}{k_r}\frac{dT}{dt}$ |
| Electrical    | Inductor         | $v=L\frac{di}{dt}$                  |
| Fluid         | Inertance        | $P=I_f\frac{dQ}{dt}$                |

#### D Type Elements

| System Type   | Element            | Elemental Equation      |
| ------------- | ------------------ | ----------------------- |
| Translational | Damper             | $v=\frac{1}{B}F$        |
| Rotational    | Rotational Damper  | $\Omega=\frac{1}{B_r}T$ |
| Electrical    | Resistor           | $v=Ri$                  |
| Fluid         | Fluid Resistance   | $P=R_fQ$                |
| Thermal       | Thermal Resistance | $T=R_tq$                |

### Linear Graph

Add each element of the system to the linear graph.
A type elements always connect to the ground.
Arrows point in the direction of decreasing across variable.

### Normal Tree

* Do not create loops
* $N-1$ branches must be selected

Here $N$ is the number of nodes in the linear graph.

1. Accross variable sources
2. A type elements
3. D type elements
4. T type elements

Normal tree branches are the elements in the normal tree, and links are the elements not in the normal tree.

### Primary Variables

* Across variables on normal tree branches
* Through variables on normal tree links

For each element the secondary variable is the non primary variable.

### State Variables

* A type elements on normal tree branches
* T type elements on normal tree links

### Elemental Equations

$B-S$ elemental equations should be written with the primary variable on the left hand side.
Here $B$ is the number of branches in the normal tree and $S$ is the number of sources.

### Continuity Equations

$N-1-S_A$ continuity equations should be found by drawing a contour around any number of nodes which cuts thourgh only one branch.
For each equation the secondary through variable should be placed on the left hand side, and the sum of the through variable flowing through the contour listed.

### Compatibility Equations

$B-N+1-S_T$ compatibility equations should be written with the secondary accross variable on the left side.
To create these equations calculate the sum of the across variables around the loop created when a normal tree link is added to the normal tree.
Do this for each normal tree link.

## Example

To show how this process works, example 5.9 in Rowell and Wormley will be worked out in detail here.

![Example 5.9](.images/Example5-9.jpg)

### Linear Graph

![Linear Graph](.images/tutorial1.svg)

### Normal Tree

![Normal Tree](.images/tutorial2.svg)

### Primary Variables

### State Variables

### Elemental Equations

### Continuity Equations

### Compatibility Equations

## Using the Software
