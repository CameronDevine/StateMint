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
Module[{allVars,elimVars,stateEqs},

(* Extract variables to eliminate *)
allVars = equations//extractFunctions;
elimVars = allVars//Complement[#,joinWDer[inVars~Join~stateVars,t]]&;

(* Eliminate non state and input variables and place in standard form *)
stateEqs = equations//Eliminate[#,elimVars]&//Solve[#,D[stateVars,t]]&//Collect[#,stateVars]&;
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
Module[{allVars,elimVars,outEqs,outEqsRaw,yOut,stateEqsID,sansStateEqsID},

(* Extract variables to eliminate *)
allVars = equations//extractFunctions;
elimVars = allVars//Complement[#,joinWDer[inVars~Join~stateVars,t]]&;

(* Solve for output expressions in terms of state and input variables*)
stateEqsID=equations//Position[#,x_'[y_],{0,Infinity}]&//Transpose//First//{#}&//Transpose;
sansStateEqsID=equations//Delete[#,stateEqsID]&;
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
	inVarsOP_List, (* operating point for input variables *)
	stateVars_List, (* state variables *)
	stateVarsOP_List, (* operating point for state variables *)
	equations_List (* rhs of nonlinear (or linear) state equation *)
]
Returns an array containing the A and B matrices {A,B} of the input state equation
linearized about the input and state operating point.";

linearizeState[inVars_List,inVarsOP_List,stateVars_List,stateVarsOP_List,equations_List]:=
Module[{a,b,stateVarsOPRules,inVarsOPRules,OPRules},
stateVarsOPRules=Thread[stateVars->stateVarsOP];
inVarsOPRules=Thread[inVars->inVarsOP];
OPRules=stateVarsOPRules~Join~inVarsOPRules;
a=equations//D[#,{stateVars}]&//ReplaceAll[#,OPRules]&; (* Jacobian wrt x *)
b=equations//D[#,{inVars}]&//ReplaceAll[#,OPRules]&;(* Jacobian wrt u *)
{a,b}//Return;
]

linearizeOutput::usage =
"linearizeOutput[
	inVars_List, (* input variables *)
	inVarsOP_List, (* operating point for input variables *)
	stateVars_List, (* state variables *)
	stateVarsOP_List, (* operating point for state variables *)
	equations_List (* rhs of nonlinear (or linear) output equation *)
]
Returns an array containing the C and D matrices {C,D} of the output equation
linearized about the input and state operating point.";

linearizeOutput[inVars_List,inVarsOP_List,stateVars_List,stateVarsOP_List,equations_List]:=
Module[{c,d,stateVarsOPRules,inVarsOPRules,OPRules},
stateVarsOPRules=Thread[stateVars->stateVarsOP];
inVarsOPRules=Thread[inVars->inVarsOP];
OPRules=stateVarsOPRules~Join~inVarsOPRules;
c=equations//D[#,{stateVars}]&//ReplaceAll[#,OPRules]&; (* Jacobian wrt x *)
d=equations//D[#,{inVars}]&//ReplaceAll[#,OPRules]&;(* Jacobian wrt u *)
{c,d}//Return;
]

extractFunctions::usage =
"extractFunctions[
	exp_ (* expression that contains function variables, e.g. vC1'[t]==1/C1*iC1[t] *)
]
Returns a list of function variables, e.g. iC1[t].";

extractFunctions[exp_]:=exp//Cases[#,x_[y_]:>x[y],{0,Infinity}]&//DeleteDuplicates;

joinWDer::usage =
"joinWDer[
	list_List, (* a list of expressions, e.g. {vC1[t],vc2[t]} *)
	t_Symbol   (* symbol with respect to which list is differentiated *)
]
Returns input list joined with its derivative, e.g. {vC1[t],vc2[t],vC1'[t],vC2'[t]}.";

joinWDer[list_List,t_Symbol]:=list~Join~D[list,t];


State::usage =
"State[
	InVars,         (* input variable names.  e.g.  vS   *)
	StVarElEqns,    (* state equations for state variable.  e.g.  vM' == 1/M fM   *)
	OtherElEqns,    (* other elemental equations. 
                                          e.g. v1 \[Equal] Km o2, or tJm = Jm oJm'   *)
	Constraints,    (* constraint expressions.  e.g.  fM \[Rule] fD - f4   *)
	OutputVars      (* output variables.  e.g.  fM   *)
]
Computes the state equations, StEqn. 
Also, gives the a, b, c, d, e, f matricies and transfer functions, TfM, for a linear state model.
StateVers=1.4 (legacy ... see stateEquations)";

State[InVarsLo_,
	StVarElEqnsLo_,
	OtherElEqnsLo_,
	ConstraintsLo_,
	OutputVarsLo_] :=Module[{i, j, St2,E3, Co2,StateEquation,StateEqsFinal,OutputEqsFinal, 
StVarsLo,StVarsLoT,OtherPriVarsLo,OtherPriVarsLoT,OtherElEqnsLoT,SecVars,SecVarsT,OutputVarsLoT,
ConstraintsLoT,StVarElEqnsLoT,InVarsLoT,
nSt,nIn,nOut,aa,bb,cc,dd,ee,ff, bbp, ddp,TT},

(* Find lists of state, other primary,  secondary, input, and output variables *)
StVarsLo=Map[Part[#,1]&,Map[Part[#,1]&,StVarElEqnsLo]];
StVarsLoT=StVarsLo/.Map[#->Apply[#,{t}]&,StVarsLo];
OtherPriVarsLo=Map[Part[#,1]&,OtherElEqnsLo];
OtherPriVarsLoT=OtherPriVarsLo/.Map[#->Apply[#,{t}]&,OtherPriVarsLo];
SecVars=Map[Part[#,1]&,ConstraintsLo];
SecVarsT=SecVars/.Map[#->Apply[#,{t}]&,SecVars];
InVarsLoT=Map[Apply[#,{t}]&,InVarsLo];
OutputVarsLoT=Map[Apply[#,{t}]&,OutputVarsLo];

(* Transform input variables, state and other primary elemental equations, and constraints into functions of time *)
StVarElEqnsLoT=StVarElEqnsLo/.Map[#->Apply[#,{t}]&,Map[Part[#,1]&,StVarElEqnsLo]];
StVarElEqnsLoT=StVarElEqnsLoT/.Map[#->Apply[#,{t}]&,SecVars];
OtherPriVarsLoT=OtherPriVarsLo/.Map[#->Apply[#,{t}]&,{SecVars,OtherPriVarsLo}//Flatten];
OtherElEqnsLoT=OtherElEqnsLo/.Map[#->Apply[#,{t}]&,Map[Part[#,1]&,OtherElEqnsLo]];
OtherElEqnsLoT=OtherElEqnsLoT/.Map[#->Apply[#,{t}]&,SecVars];
(* OtherElEqnsLoT=Map[StringReplace[ToString[#,InputForm],"["<>ToString[t]<>"]]"->"]["<>ToString[t]<>"]"]&,OtherElEqnsLoT]//ToExpression; *)
ConstraintsLoT=ConstraintsLo/.Map[#->Apply[#,{t}]&,{StVarsLo,SecVars,OtherPriVarsLo,InVarsLo}//Flatten];

(*  Substitute cut-set and tie-set equations (along with any necessary derivatives) into all elemental equations. Solve for the Other primary variables,in terms of state variables  *)
St2=StVarElEqnsLoT/.Flatten[{ConstraintsLoT,D[ConstraintsLoT,t]}];
Co2=OtherElEqnsLoT/.Flatten[{ConstraintsLoT,D[ConstraintsLoT,t]}];
OtherPriVarsLoT=OtherPriVarsLoT;
E3=Solve[Flatten[{Co2,D[Co2,t]}],Flatten[{OtherPriVarsLoT,D[OtherPriVarsLoT,t]}]][[1]]//
Simplify;

(*  Eliminate the non-state variables in the state equations  *)

StateEquation=St2/.E3//
Solve[#,D[StVarsLoT,t]][[1]]& //
Simplify;
StateEqsFinal=D[StVarsLoT,t]/.StateEquation;
OutputEqsFinal=OutputVarsLoT/.ConstraintsLoT/.E3/.StateEquation//Simplify;

(*  Extract the state matricies: a, b, c, d, e, and f  *)

nSt=Length[StVarsLoT];
nIn=Length[InVarsLoT];
nOut=Length[OutputEqsFinal];
Clear[ aa,bb,cc,dd];
aa=Table[0,{nSt},{nSt}];
For[i=1,i<=nSt,i++,
For[j=1, j<=nSt,j++,
aa[[i,j]]=D[ StateEqsFinal[[i]],StVarsLoT[[j]] ];
];
];
bb=Table[0,{nSt},{nIn}];
For[i=1,i<=nSt,i++,
For[j=1, j<=nIn,j++,
bb[[i,j]]=D[ StateEqsFinal[[i]],InVarsLoT[[j]] ];
];
];
cc=Table[0,{nOut},{nSt}];
For[i=1,i<=nOut,i++,
For[j=1, j<=nSt,j++,
cc[[i,j]]=D[ OutputEqsFinal[[i]],StVarsLoT[[j]] ];
];
];
dd=Table[0,{nOut},{nIn}];
For[i=1,i<=nOut,i++,
For[j=1, j<=nIn,j++,
dd[[i,j]]=D[ OutputEqsFinal[[i]],InVarsLoT[[j]] ];
];
];
ee=Table[0,{nSt},{nIn}];
For[i=1,i<=nSt,i++,
For[j=1, j<=nIn,j++,
ee[[i,j]]=D[ StateEqsFinal[[i]],D[InVarsLoT,t][[j]] ];
];
];
ff=Table[0,{nOut},{nIn}];
For[i=1,i<=nOut,i++,
For[j=1, j<=nIn,j++,
ff[[i,j]]=D[ OutputEqsFinal[[i]],D[InVarsLoT,t][[j]] ];
];
];

(* Compute the transfer function matrix, 
	accounting for possible nonstandard state model *)
bbp=(aa.ee+bb);
ddp=(cc.ee+dd);
TT=cc.Inverse[s IdentityMatrix[nSt]-aa].bbp+ddp+ff s//Simplify;
a=aa;
b=bb;
c=cc;
d=dd;
e=ee;
f=ff;
TfM=TT;
StVars=StVarsLoT;
StEqn=StateEqsFinal;
StateVers=1.3;
{a,b,c,d,e,f,TfM,StEqn,StateVers}
(* 
a=OutputEqsFinal;
{a}*)
];

EndPackage[];
