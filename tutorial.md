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

| System Type   | Element            | Elemental Equation
| ------------- | ------------------ | ------------------
| Translational | Mass               | ![F=m\frac{dv}{dt}](http://latex.codecogs.com/svg.latex?F%3Dm%5Cfrac%7Bdv%7D%7Bdt%7D)
| Rotational    | Inertia            | ![\tau=J\frac{d\Omega}{dt}](http://latex.codecogs.com/svg.latex?%5Ctau%3DJ%5Cfrac%7Bd%5COmega%7D%7Bdt%7D)
| Electrical    | Capacitor          | ![i=C\frac{dv}{dt}](http://latex.codecogs.com/svg.latex?i%3DC%5Cfrac%7Bdv%7D%7Bdt%7D)
| Fluid         | Fluid Capacitor    | ![Q=C_f\frac{dP}{dt}](http://latex.codecogs.com/svg.latex?Q%3DC_f%5Cfrac%7BdP%7D%7Bdt%7D)
| Thermal       | Thermal Capictance | ![q=C_t\frac{dT}{dt}](http://latex.codecogs.com/svg.latex?q%3DC_t%5Cfrac%7BdT%7D%7Bdt%7D)

#### T Type Elements

| System Type   | Element          | Elemental Equation
| ------------- | ---------------- | ------------------
| Translational | Spring           | ![v=\frac{1}{K}\frac{dF}{dt}](http://latex.codecogs.com/svg.latex?v%3D%5Cfrac%7B1%7D%7BK%7D%5Cfrac%7BdF%7D%7Bdt%7D)
| Rotational    | Torsional Spring | ![\Omega=\frac{1}{k_r}\frac{d\tau}{dt}](http://latex.codecogs.com/svg.latex?%5COmega%3D%5Cfrac%7B1%7D%7Bk_r%7D%5Cfrac%7Bd%5Ctau%7D%7Bdt%7D)
| Electrical    | Inductor         | ![v=L\frac{di}{dt}](http://latex.codecogs.com/svg.latex?v%3DL%5Cfrac%7Bdi%7D%7Bdt%7D)
| Fluid         | Inertance        | ![P=I_f\frac{dQ}{dt}](http://latex.codecogs.com/svg.latex?P%3DI_f%5Cfrac%7BdQ%7D%7Bdt%7D)

#### D Type Elements

| System Type   | Element            | Elemental Equation
| ------------- | ------------------ | ------------------
| Translational | Damper             | ![v=\frac{1}{B}F](http://latex.codecogs.com/svg.latex?v%3D%5Cfrac%7B1%7D%7BB%7DF)
| Rotational    | Rotational Damper  | ![\Omega=\frac{1}{B_r}\tau](http://latex.codecogs.com/svg.latex?%5COmega%3D%5Cfrac%7B1%7D%7BB_r%7D%5Ctau)
| Electrical    | Resistor           | ![v=Ri](http://latex.codecogs.com/svg.latex?v%3DRi)
| Fluid         | Fluid Resistance   | ![P=R_fQ](http://latex.codecogs.com/svg.latex?P%3DR_fQ)
| Thermal       | Thermal Resistance | ![T=R_tq](http://latex.codecogs.com/svg.latex?T%3DR_tq)

### Linear Graph

Add each element of the system to the linear graph.
A type elements always connect to the ground.
Arrows point in the direction of decreasing across variable.

### Normal Tree

* Do not create loops
* ![N-1](http://latex.codecogs.com/svg.latex?N-1) branches must be selected

Here ![N](http://latex.codecogs.com/svg.latex?N) is the number of nodes in the linear graph.

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

![B-S](http://latex.codecogs.com/svg.latex?B-S) elemental equations should be written with the primary variable on the left hand side.
Here ![B](http://latex.codecogs.com/svg.latex?B) is the number of branches in the normal tree and ![S](http://latex.codecogs.com/svg.latex?S) is the number of sources.

### Continuity Equations

![N-1-S_A](http://latex.codecogs.com/svg.latex?N-1-S_A) continuity equations should be found by drawing a contour around any number of nodes which cuts thourgh only one branch.
For each equation the secondary through variable should be placed on the left hand side, and the sum of the through variable flowing through the contour listed.

### Compatibility Equations

![B-N+1-S_T](http://latex.codecogs.com/svg.latex?B-N%2B1-S_T) compatibility equations should be written with the secondary accross variable on the left side.
To create these equations calculate the sum of the across variables around the loop created when a normal tree link is added to the normal tree.
Do this for each normal tree link.

## Example

To show how this process works, we will work through the following example.

![Example System](.images/tutorial1.svg)

This system is a voltage source which drives a motor with the given resistance and inductance.
This motor in turn drives a pump through a driveshaft with the given stiffness.
Finall the pump pushes water through a curved pipe of known resistance.

### Linear Graph

This system can be distilled into the linear graph below.

![Linear Graph](.images/tutorial2.svg)

### Normal Tree

To create the normal tree, first the voltage source is selected.

![Normal Tree](.images/tutorial3.svg)

To avoid selecting the torsional spring both sides of the gyrator added to the normal tree.

![Normal Tree](.images/tutorial5.svg)

Since one side of the transformer must be added to the normal tree, the left side is added.

![Normal Tree](.images/tutorial6.svg)

Finally to complete the normal tree the motor resistance is added.

![Normal Tree](.images/tutorial7.svg)

### Primary Variables

![V_s](http://latex.codecogs.com/svg.latex?V_s),
![v_R](http://latex.codecogs.com/svg.latex?v_R),
![i_L](http://latex.codecogs.com/svg.latex?i_L),
![v_1](http://latex.codecogs.com/svg.latex?v_1),
![\tau_2](http://latex.codecogs.com/svg.latex?%5Ctau_2),
![\tau_k](http://latex.codecogs.com/svg.latex?%5Ctau_k),
![\Omega_3](http://latex.codecogs.com/svg.latex?%5COmega_3),
![P_4](http://latex.codecogs.com/svg.latex?P_4),
![Q_R](http://latex.codecogs.com/svg.latex?Q_R)

### Secondary Variables

![i_s](http://latex.codecogs.com/svg.latex?i_s),
![i_R](http://latex.codecogs.com/svg.latex?i_R),
![v_L](http://latex.codecogs.com/svg.latex?v_L),
![i_1](http://latex.codecogs.com/svg.latex?i_1),
![\Omega_2](http://latex.codecogs.com/svg.latex?%5COmega_2),
![\Omega_k](http://latex.codecogs.com/svg.latex?%5COmega_k),
![Q_4](http://latex.codecogs.com/svg.latex?Q_4),
![P_R](http://latex.codecogs.com/svg.latex?P_R)

### State Variables

![i_L](http://latex.codecogs.com/svg.latex?i_L),
![\tau_k](http://latex.codecogs.com/svg.latex?%5Ctau_k)

### Elemental Equations

* ![v_R=Ri_R](http://latex.codecogs.com/svg.latex?v_R%3DRi_R)
* ![\frac{di_L}{dt}=\frac{v_L}{L}](http://latex.codecogs.com/svg.latex?%5Cfrac%7Bdi_L%7D%7Bdt%7D%3D%5Cfrac%7Bv_L%7D%7BL%7D)
* ![v_1=\frac{\Omega_2}{K_v}](http://latex.codecogs.com/svg.latex?v_1%3D%5Cfrac%7B%5COmega_2%7D%7BK_v%7D)
* ![\tau_2=\frac{i_1}{-K_v}](http://latex.codecogs.com/svg.latex?%5Ctau_2%3D%5Cfrac%7Bi_1%7D%7B-K_v%7D)
* ![\frac{d\tau_k}{dt}=k_t\Omega_k](http://latex.codecogs.com/svg.latex?%5Cfrac%7Bd%5Ctau_k%7D%7Bdt%7D%3Dk_t%5COmega_k)
* ![\Omega_3=\frac{Q_4}{-D}](http://latex.codecogs.com/svg.latex?%5COmega_3%3D%5Cfrac%7BQ_4%7D%7B-D%7D)
* ![P_4=\frac{\tau_3}{D}](http://latex.codecogs.com/svg.latex?P_4%3D%5Cfrac%7B%5Ctau_3%7D%7BD%7D)
* ![Q_R=\frac{P_R}{R_f}](http://latex.codecogs.com/svg.latex?Q_R%3D%5Cfrac%7BP_R%7D%7BR_f%7D)

### Continuity Equations

![Normal Tree](.images/tutorial8.svg)

* ![i_R=i_L](http://latex.codecogs.com/svg.latex?i_R%3Di_L)
* ![i_s=i_L](http://latex.codecogs.com/svg.latex?i_s%3Di_L)
* ![i_1=i_l](http://latex.codecogs.com/svg.latex?i_1%3Di_l)
* ![\tau_3=-\tau_k-\tau_2](http://latex.codecogs.com/svg.latex?%5Ctau_3%3D-%5Ctau_k-%5Ctau_2)
* ![Q_4=Q_R](http://latex.codecogs.com/svg.latex?Q_4%3DQ_R)

### Compatibility Equations

* ![v_L=V_s-v_R-v_1](http://latex.codecogs.com/svg.latex?v_L%3DV_s-v_R-v_1)
* ![\Omega_2=\Omega_3](http://latex.codecogs.com/svg.latex?%5COmega_2%3D%5COmega_3)
* ![\Omega_k=\Omega_3](http://latex.codecogs.com/svg.latex?%5COmega_k%3D%5COmega_3)
* ![P_R=P_4](http://latex.codecogs.com/svg.latex?P_R%3DP_4)

## Using the Software
