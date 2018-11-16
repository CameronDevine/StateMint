(* ::Package:: *)

BeginPackage["State`"];


stateEquations::usage =
"stateEquations[
	inVars_List,    (* input variable names, e.g. vS[t] *)
	stateVars_List, (* state variable names, e.g. vC1[t] *)
	equations_List  (* first-order ode and algebraic eqs, e.g. vC1'[t]==1/C1*iC1[t] *)
]
Returns the rhs of the state equations as a list.
N.b. can handle some nonlinear systems.
N.b. a common mistake is to place the prime after the argument, but it should appear before, e.g. vC2'[t].
N.b. another common mistake is to use the assignment operator '=' instead of the boolean equals '==' in equations.
N.b. the arrangement of the equations (i.e. lhs/rhs) is immaterial.
N.b. for the output equations, use the function outEquations instead.
N.b. to linearize the returned state equations, use the function linearizeState.";

stateEquations[inVars_List,stateVars_List,equations_List] :=
Module[{allVars,elimVars,stateEqs,equationsToSolve},

(* Join with derivatives of equations in order to handle non-standard state equations *)
equationsToSolve = joinWDer[equations,t];

(* Extract variables to eliminate *)
allVars = equationsToSolve//extractFunctions;
elimVars = allVars//Complement[#,joinWDer[stateVars~Join~inVars,t]]&;

(* Eliminate non state and input variables and place in standard form *)
stateEqs = equationsToSolve//Eliminate[#,elimVars]&//Solve[#,D[stateVars,t]]&//Collect[#,stateVars]&;
stateVars//D[#,t]&//ReplaceAll[#,stateEqs]&//Flatten//Return;
];


outEquations::usage =
"outEquations[
	inVars_List,    (* input variable names, e.g. vS[t] *)
	stateVars_List, (* state variable names, e.g. vC1[t] *)
	outExps_List,   (* output expressions, e.g. vR2[t]+3*vC1[t] *)
	equations_List  (* first-order ode and algebraic eqs, e.g. vC1'[t]==1/C1*iC1[t] *)
]
Returns the rhs of the output equations as a list.
N.b. can handle some nonlinear systems.
N.b. can handle any expressions in outExps as long as they are expressed in terms of variables included in the
equations list. These are *not* limited to state variables! They can be primary or secondary and expressions thereof.
N.b. a common mistake is to place the prime after the argument, but it should appear before, e.g. vC2'[t].
N.b. another common mistake is to use the assignment operator '=' instead of the boolean equals '==' in equations.
N.b. the arrangement of the equations (i.e. lhs/rhs) is immaterial.
N.b. for the state equations, use the function stateEquations instead.
N.b. to linearize the returned output equations, use the function linearizeOutput.";

outEquations[inVars_List,stateVars_List,outExps_List,equations_List]:=
Module[{allVars,elimVars,outEqs,outEqsRaw,yOut,stateEqsID,sansStateEqsID,equationsToSolve},

(* Join with derivatives of equations in order to handle non-standard state equations *)
equationsToSolve = joinWDer[equations,t];

(* Extract variables to eliminate *)
allVars = equationsToSolve//extractFunctions;
elimVars = allVars//Complement[#,stateVars~Join~joinWDer[inVars,t]]&;

(* Toss the equations with derivatives *)
stateEqsID=equations//
	Position[#,x_'[y_],{0,Infinity}]&// (* dependent energy storage elements' elemental equations are also discarded, which seems not to matter *)
		{#}[[All,1]]&//
			Transpose;
sansStateEqsID=equations//Delete[#,stateEqsID]&;

(* Solve for output expressions in terms of state and input variables*)
yOut=Table[y[i],{i,1,Length[outExps]}];
outEqsRaw=Thread[yOut==outExps];
outEqs=(outEqsRaw~Join~sansStateEqsID)//
	Eliminate[#,elimVars]&//
		Solve[#,yOut]&//
			Collect[#,stateVars]&;
yOut/.outEqs//Flatten//Return;
]


linearizeState::usage =
"linearizeState[
	inVars_List, (* input variables *)
	stateVars_List, (* state variables *)
	equations_List, (* rhs of nonlinear (or linear) state equation *)
	inVarsOP_List: default: zeros, (* operating point for input variables *)
	stateVarsOP_List: default: zeros (* operating point for state variables *)
]
Returns an array containing the A, B, and if applicable E matrices {A,B,E} of the input state equation
linearized about the input and state operating point.";

linearizeState[
	inVars_List,
	stateVars_List,
	equations_List,
	inVarsOP_List:ConstantArray[0,Dimensions[inVars]],
	stateVarsOP_List:ConstantArray[0,Dimensions[stateVars]]
]:=
Module[{a,b,e,stateVarsOPRules,inVarsOPRules,OPRules},
stateVarsOPRules=Thread[stateVars->stateVarsOP];
inVarsOPRules=Thread[inVars->inVarsOP];
OPRules=stateVarsOPRules~Join~inVarsOPRules;
a=equations//D[#,{stateVars}]&//ReplaceAll[#,OPRules]&; (* Jacobian wrt x *)
b=equations//D[#,{inVars}]&//ReplaceAll[#,OPRules]&;(* Jacobian wrt u *)
e=equations//D[#,{D[inVars,t]}]&// (* Jacobian wrt u' *)
	ReplaceAll[#,(# -> 0)&/@D[inVars,t]]&// (* u OP a constant so u' OP is 0 *)
		ReplaceAll[#,OPRules]&; (* apply OP *)
{a,b,e}//Return;
]


linearizeOutput::usage =
"linearizeOutput[
	inVars_List, (* input variables *)
	stateVars_List, (* state variables *)
	equations_List, (* rhs of nonlinear (or linear) output equation *)
	inVarsOP_List: default: zeros, (* operating point for input variables *)
	stateVarsOP_List: default: zeros (* operating point for state variables *)
]
Returns an array containing the C, D, and if applicable F matrices {C,D,F} of the output equation
linearized about the input and state operating point.";

linearizeOutput[
	inVars_List,
	stateVars_List,
	equations_List,
	inVarsOP_List:ConstantArray[0,Dimensions[inVars]],
	stateVarsOP_List:ConstantArray[0,Dimensions[stateVars]]
]:=
Module[{c,d,f,stateVarsOPRules,inVarsOPRules,OPRules},
stateVarsOPRules=Thread[stateVars->stateVarsOP];
inVarsOPRules=Thread[inVars->inVarsOP];
OPRules=stateVarsOPRules~Join~inVarsOPRules;
c=equations//D[#,{stateVars}]&//ReplaceAll[#,OPRules]&; (* Jacobian wrt x *)
d=equations//D[#,{inVars}]&//ReplaceAll[#,OPRules]&;(* Jacobian wrt u *)
f=equations//D[#,{D[inVars,t]}]&// (* Jacobian wrt u' *)
	ReplaceAll[#,(# -> 0)&/@D[inVars,t]]&// (* u OP a constant so u' OP is 0 *)
		ReplaceAll[#,OPRules]&; (* apply OP *)
{c,d,f}//Return;
]


Begin["`Private`"];
(* private functions for internal package use *)


extractFunctions::usage =
"extractFunctions[
	exp_ (* expression that contains function variables, e.g. vC1'[t]==1/C1*iC1[t] *)
]
Returns a list of function variables, e.g. iC1[t].";

extractFunctions[exp_,var_:t]:=exp//Cases[#,x_[var]:>x[var],{0,Infinity}]&//DeleteDuplicates;


joinWDer::usage =
"joinWDer[
	list_List, (* a list of expressions, e.g. {vC1[t],vc2[t]} *)
	t_Symbol   (* symbol with respect to which list is differentiated *)
]
Returns input list joined with its derivative, e.g. {vC1[t],vc2[t],vC1'[t],vC2'[t]}.";

joinWDer[list_List,t_Symbol]:=(list~Join~(D[#,t]&/@list));
