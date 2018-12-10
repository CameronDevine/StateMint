# StateMint

_StateMint_ is a Mathematica package for assisting in the derivation of the equations of state for a dynamic system. It was originally developed by Joseph L. Garbini at the University of Washington, who continues to contribute to its development, along with Rico A.R. Picone of Saint Martin's University and Cameron N. Devine of the University of Washington. It has nearly identical functionality to the corresponding [Python](../python) and [web](../web) versions of this project. 

## Installation

Clone or download this repository. 

To fully install, copy the `StateMint.m` Mathematica package file to a directory in your Mathematica *path* (to see which directories are in your path, evaluate `$Path` in a Mathematica notebook). It is recommended to use the path that is returned by Mathematica when you evaluate `FileNameJoin[{$UserBaseDirectory, "Applications"}]`.

Another option for full installation is to 

- open Mathematica, 
- select `File > Install...`, 
- select `Package` from the `Type of Item to Install` menu,
- select `StateMint.m` from the `Source > File...` dialog, and
- select `OK`.

Once `StateMint` is fully installed, it can be loaded into a Mathematica notebook with the command

```mathematica
<<StateMint`
```

A third option is loading the package from the working directory, which can be set to the notebook's directory with the command

```mathematica
SetDirectory[NotebookDirectory[]];
```

If `StateMint.m` is then placed in the same directory as the notebook, it can be loaded with the same command (``<<StateMint` ``) without requiring full installation.

## Usage

The package has only five public functions. The usage of the four most important are described in the following sections.

### State equations: `stateEquations`

The set of state equations can be found from four arguments of the function `stateEquations`, all lists, described below.

```mathematica
stateEquations[
  inVars_List,              (* input variable names, e.g. vS[t] *)
  primaryVars_List,         (* primary variable names, e.g. vC1[t] *)
  elementalEquations_List,  (* elemental equations *)
  constraintEquations_List  (* constraint equations, i.e. continuity and compatibility equations *)
]
```

This function returns a list of replacement rules:

```mathematica
{
  "state variables" -> stateVars, (* a list of state variables in the order of the state equations *) 
  "RHS" -> rhs,                   (* the right-hand sides of the state equations *)
  "state equations" -> eqs        (* the full state equations *)
}
```

Here's a quick example, taken from the unit tests. First, from the linear graph, we define the relevant variables and equations.

```mathematica
inVars = { (* input variables *)
  Vs[t]
};
primaryVars = { (* primary variables *)
  vC[t],
  iL[t],
  iR[t]
};
elementalEqs = { (* elemental equations *)
  vC'[t] == iC[t]/CC,
  iL'[t] == vL[t]/L,
  iR[t] == vR[t]/R
};
constraintEqs = { (* continuity and compatibility equations *)
  iC[t] == iR[t] - iL[t],
  vL[t] == vC[t],
  vR[t] == Vs[t] - vC[t]
};
```

At this time, all variables must be functions of time `t`.

Now we apply `stateEquations`. 

```mathematica
stateSolution = stateEquations[
  inVars_List,              (* input variable names, e.g. vS[t] *)
  primaryVars_List,         (* primary variable names, e.g. vC1[t] *)
  elementalEquations_List,  (* elemental equations *)
  constraintEquations_List  (* continuity and compatibility equations *)
]
```

The returned list of replacement rules `stateSolution` can be used to assign the returned lists to individual variables or display the results, as we do in the following.

```mathematica
stateVars = "state variables" /. stateSolution;
stateEqList = "RHS" /. stateSolution;
"state equations" /. stateSolution // TableForm
```

The last statement prints a version of the following list of state equations.

<a href="https://www.codecogs.com/eqnedit.php?latex=\begin{align*}&space;\text{vC}'(t)&=-\frac{\text{iL}(t)}{\text{CC}}-\frac{\text{vC}(t)}{\text{CC}&space;R}&plus;\frac{\text{Vs}(t)}{\text{CC}&space;R}\\&space;\text{iL}'(t)&=\frac{\text{vC}(t)}{L}&space;\end{align*}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{align*}&space;\text{vC}'(t)&=-\frac{\text{iL}(t)}{\text{CC}}-\frac{\text{vC}(t)}{\text{CC}&space;R}&plus;\frac{\text{Vs}(t)}{\text{CC}&space;R}\\&space;\text{iL}'(t)&=\frac{\text{vC}(t)}{L}&space;\end{align*}" title="\begin{align*} \text{vC}'(t)&=-\frac{\text{iL}(t)}{\text{CC}}-\frac{\text{vC}(t)}{\text{CC} R}+\frac{\text{Vs}(t)}{\text{CC} R}\\ \text{iL}'(t)&=\frac{\text{vC}(t)}{L} \end{align*}" /></a>

### Output equations: `outputEquations`

The output equations are derived from a list of expressions in terms of primary and/or secondary variables. In general, these expressions can be of any algebraic form (with some nonlinear expressions supported) and need not necessarily be single variables, like those chosen below.

```mathematica
outExps = { (* output expressions *)
  iR[t],
  vR[t],
  vL[t],
  iC[t]
};
```

Now we can apply the function `outputEquations` to solve for the output equations as follows.

```mathematica
outEqList = outEquations[
  inVars, 
  stateVars, 
  outExps, 
  elementalEqs~Join~constraintEqs
];
```

The returned `outEqList` is a list of the expressions of `outExps` in terms of state variables `stateVars` and input variables `outExps`.
To display this list, use the following statement.

```mathematica
outEqList // 
  Thread[Table[y[i], {i, 1, Length[outExps]}] == #] & //
    TableForm
```

The output looks something like the following.

<a href="https://www.codecogs.com/eqnedit.php?latex=\begin{align*}&space;y_1&=\frac{\text{Vs}(t)}{R}-\frac{\text{vC}(t)}{R}\\&space;y_2&=\text{Vs}(t)-\text{vC}(t)\\&space;y_3&=\text{vC}(t)\\&space;y_4&=-\text{iL}(t)-\frac{\text{vC}(t)}{R}&plus;\frac{\text{Vs}(t)}{R}&space;\end{align*}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{align*}&space;y_1&=\frac{\text{Vs}(t)}{R}-\frac{\text{vC}(t)}{R}\\&space;y_2&=\text{Vs}(t)-\text{vC}(t)\\&space;y_3&=\text{vC}(t)\\&space;y_4&=-\text{iL}(t)-\frac{\text{vC}(t)}{R}&plus;\frac{\text{Vs}(t)}{R}&space;\end{align*}" title="\begin{align*} y_1&=\frac{\text{Vs}(t)}{R}-\frac{\text{vC}(t)}{R}\\ y_2&=\text{Vs}(t)-\text{vC}(t)\\ y_3&=\text{vC}(t)\\ y_4&=-\text{iL}(t)-\frac{\text{vC}(t)}{R}+\frac{\text{Vs}(t)}{R} \end{align*}" /></a>

### Linearize the state equations: `linearizeState`

The function `linearizeState` linearizes (if necessary) a state equation and returns the matrix coefficients of the state vector, input vector, and time-derivative of the input vector, traditionally denoted A, B, and E. It accepts a list of the right-hand sides of the the state equations (we defined above as `stateEqList`), which was returned by `stateEquations` as a replacement rule for `"RHS"`; a list of state variables (we defined above as `stateVars`), which was returned by `stateEquations` as a replacement rule for `"state variables"`; and the input variables `inVars`. Let's consider its inputs in more detail.

```mathematica
linearizeState[
  inVars_List,      (* input variables *)
  stateVars_List,   (* state variables *)
  equations_List,   (* rhs of nonlinear (or linear) state equation *)
  inVarsOP_List,    (* OPTIONAL operating point for input variables *)
  stateVarsOP_List  (* OPTIONAL operating point for state variables *)
]
```

The last two arguments are optional and define the operating point for linearization, zero by default. Returning to our example, our state equations are already linear, but we'd like to automatically extract the A, B, and E matrices.

```mathematica
abe = linearizeState[inVars, stateVars, stateEqList];
{a,b,e} = abe; (* break out each matrix, if desired *)
```

The function returned a list of lists representing the A, B, and E matrices (`a`, `b`, and `e`). Print them as follows.

```mathematica
Table[
  Print[
    {"A", "B", "E"}[[i]] <> " = ",
    abe[[i]] // MatrixForm
  ],
  {i, 1, 3}
];
```

The output looks something like the following.

<a href="https://www.codecogs.com/eqnedit.php?latex=\begin{align*}&space;A&space;&=&space;\left[&space;\begin{array}{cc}&space;-\frac{1}{\text{CC}&space;R}&space;&&space;-\frac{1}{\text{CC}}&space;\\&space;\frac{1}{L}&space;&&space;0&space;\\&space;\end{array}&space;\right]\\&space;B&space;&=\left[&space;\begin{array}{c}&space;\frac{1}{\text{CC}&space;R}&space;\\&space;0&space;\\&space;\end{array}&space;\right]&space;\\&space;E&space;&=&space;\left[&space;\begin{array}{c}&space;0&space;\\&space;0&space;\\&space;\end{array}&space;\right]&space;\end{align*}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{align*}&space;A&space;&=&space;\left[&space;\begin{array}{cc}&space;-\frac{1}{\text{CC}&space;R}&space;&&space;-\frac{1}{\text{CC}}&space;\\&space;\frac{1}{L}&space;&&space;0&space;\\&space;\end{array}&space;\right]\\&space;B&space;&=\left[&space;\begin{array}{c}&space;\frac{1}{\text{CC}&space;R}&space;\\&space;0&space;\\&space;\end{array}&space;\right]&space;\\&space;E&space;&=&space;\left[&space;\begin{array}{c}&space;0&space;\\&space;0&space;\\&space;\end{array}&space;\right]&space;\end{align*}" title="\begin{align*} A &= \left[ \begin{array}{cc} -\frac{1}{\text{CC} R} & -\frac{1}{\text{CC}} \\ \frac{1}{L} & 0 \\ \end{array} \right]\\ B &=\left[ \begin{array}{c} \frac{1}{\text{CC} R} \\ 0 \\ \end{array} \right] \\ E &= \left[ \begin{array}{c} 0 \\ 0 \\ \end{array} \right] \end{align*}" /></a>

### Linearize the output equations: `linearizeOutput`

The function `linearizeOutput` is very similar to `linearizeState`, but linearizes (if necessary) an output equation and returns the matrix coefficients of the state vector, input vector, and time-derivative of the input vector, traditionally denoted C, D, and F. It accepts a list of the right-hand sides of the the output equations (we defined above as `stateEqList`), which was returned by `outputEquations`; a list of state variables (we defined above as `stateVars`), which was returned by `stateEquations` as a replacement rule for `"state variables"`; and the input variables `inVars`. Let's consider its inputs in more detail.

```mathematica
linearizeOutput[
  inVars_List,      (* input variables *)
  stateVars_List,   (* state variables *)
  equations_List,   (* rhs of nonlinear (or linear) output equation *)
  inVarsOP_List,    (* OPTIONAL operating point for input variables *)
  stateVarsOP_List  (* OPTIONAL operating point for state variables *)
]
```

The last two arguments are optional and define the operating point for linearization, zero by default. Returning to our example, our state equations are already linear, but we'd like to automatically extract the C, D, and F matrices.

```mathematica
cdf = linearizeOutput[inVars, stateVars, outputEqList];
{c,d,f} = cdf; (* break out each matrix, if desired *)
```

The function returned a list of lists representing the C, D, and F matrices (`c`, `d`, and `f`). Print them as follows.

```mathematica
Table[
  Print[
    {"C", "D", "F"}[[i]] <> " = ",
    cdf[[i]] // MatrixForm
  ],
  {i, 1, 3}
];
```

The output looks something like the following.

<a href="https://www.codecogs.com/eqnedit.php?latex=\begin{align*}&space;C&space;&=&space;\left[&space;\begin{array}{cc}&space;-\frac{1}{R}&space;&&space;0&space;\\&space;-1&space;&&space;0&space;\\&space;1&space;&&space;0&space;\\&space;-\frac{1}{R}&space;&&space;-1&space;\\&space;\end{array}&space;\right]\\&space;D&space;&=&space;\left[&space;\begin{array}{c}&space;\frac{1}{R}&space;\\&space;1&space;\\&space;0&space;\\&space;\frac{1}{R}&space;\\&space;\end{array}&space;\right]&space;\\&space;F&space;&=&space;\left[&space;\begin{array}{c}&space;0&space;\\&space;0&space;\\&space;0&space;\\&space;0&space;\\&space;\end{array}&space;\right]&space;\end{align*}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{align*}&space;C&space;&=&space;\left[&space;\begin{array}{cc}&space;-\frac{1}{R}&space;&&space;0&space;\\&space;-1&space;&&space;0&space;\\&space;1&space;&&space;0&space;\\&space;-\frac{1}{R}&space;&&space;-1&space;\\&space;\end{array}&space;\right]\\&space;D&space;&=&space;\left[&space;\begin{array}{c}&space;\frac{1}{R}&space;\\&space;1&space;\\&space;0&space;\\&space;\frac{1}{R}&space;\\&space;\end{array}&space;\right]&space;\\&space;F&space;&=&space;\left[&space;\begin{array}{c}&space;0&space;\\&space;0&space;\\&space;0&space;\\&space;0&space;\\&space;\end{array}&space;\right]&space;\end{align*}" title="\begin{align*} C &= \left[ \begin{array}{cc} -\frac{1}{R} & 0 \\ -1 & 0 \\ 1 & 0 \\ -\frac{1}{R} & -1 \\ \end{array} \right]\\ D &= \left[ \begin{array}{c} \frac{1}{R} \\ 1 \\ 0 \\ \frac{1}{R} \\ \end{array} \right] \\ F &= \left[ \begin{array}{c} 0 \\ 0 \\ 0 \\ 0 \\ \end{array} \right] \end{align*}" /></a>


## Getting started

The example notebook `Example.nb` shows an application. Open it in Mathematica and run them. It works without fully installing the package.

An extensive example of a hydroelectric power generation system can be found [here](http://ricopic.one/dynamic_systems/source/microhydroelectric.nb).
