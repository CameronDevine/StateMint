'''Regression tests: every worked state-space model in the System Dynamics notes.

Each test transcribes one model from the notes (Rico Picone, *System Dynamics*,
repository ``system-dynamics-book/systems-parody``) into StateMint's five input
lists and checks the matrices the notes report.

Conventions
-----------
* The input lists follow the notes' step 1 (Rowell & Wormley ch. 5): the
  state-variable elemental equations solved for the state derivative, the other
  elemental equations solved for the primary variable, and the continuity and
  compatibility equations solved for the secondary variable. State equations
  are listed in the notes' order of the state vector, so A matches entry by
  entry.
* Subscripts are dropped: v_C -> vC, F_{K_1} -> FK1, Omega_J -> WJ,
  T_{K_r} -> TKr, Omega_s -> Ws. A source's delivered through-variable that the
  notes write as i_s is iS (``is`` is a Python keyword).
* Outputs are written as the notes write them, expressions included. Where
  the notes obtain an output from a continuity equation at a source's node
  (3.4 footnote 5: "We write that equation only when it is an output"), that
  equation is added to the constraints.
  StateMint 2.1.1 parsed each output as ``name(t)``, so of these only
  ``m1*vm1``-style products ending in the variable came out right; the
  door, seat, trailer, blowhard, tetris and rectangle tests fail on 2.1.1.
* Models in standard form are also checked for E = F = 0.
* Where the notes are wrong (see the NOTES ERRATUM comments), the test asserts
  the corrected value and the comment quotes what the notes print.

Notes paths below are relative to ``systems-parody/chapters/``.
'''

import sympy
import pytest
from sympy.core.function import AppliedUndef

import StateMint


# --------------------------------------------------------------------------
# helpers

def solve(inputs, st_eqs, other_eqs, constraints, outputs):
	return StateMint.Solve(inputs, st_eqs, other_eqs, constraints, outputs)


def _plain(expr):
	'''Replace f(t) by the symbol f and d f(t)/dt by the symbol f_dot.'''
	expr = sympy.sympify(expr)
	reps = {}
	for d in expr.atoms(sympy.Derivative):
		if isinstance(d.expr, AppliedUndef):
			reps[d] = sympy.Symbol(d.expr.func.__name__ + '_dot')
	expr = expr.xreplace(reps)
	reps = {f: sympy.Symbol(f.func.__name__) for f in expr.atoms(AppliedUndef)}
	return expr.xreplace(reps)


def assert_matrix(name, got, expected):
	expected = sympy.Matrix(expected)
	got = sympy.Matrix(_plain(got))
	assert got.shape == expected.shape, (
		'{}: shape {} != expected {}\n got {}'.format(
			name, got.shape, expected.shape, got))
	diff = sympy.simplify(got - expected)
	assert diff == sympy.zeros(*expected.shape), (
		'{} mismatch\n got      {}\n expected {}'.format(name, got, expected))


def check(sys, **expected):
	'''check(sys, A=..., B=..., ...): compare each named attribute.'''
	for name, value in expected.items():
		assert_matrix(name, getattr(sys, name), value)


def check_standard_form(sys):
	'''No input derivatives: E and F are zero.'''
	assert_matrix('E', sys.E, sympy.zeros(*sys.B.shape))
	assert_matrix('F', sys.F, sympy.zeros(*sys.D.shape))


# The web interface's field splitter (commas outside parentheses, new lines).
split_field = StateMint.split_entries


def solve_rnd(fields):
	return solve(*(split_field(fields[k]) for k in (
		'InVars', 'StVarElEqns', 'OtherElEqns', 'Constraints', 'OutputVars')))


# --------------------------------------------------------------------------
# Chapter 3, state-and-output-equations.md (3.2, ex:door-matrices) with the
# derivation of problems.md#pacman

def test_3_2_door_and_pacman():
	'''3.2 state-and-output-equations.md, ex:door-matrices (outputs and C, D)
	with the elemental and constraint equations of state-space-models/
	problems.md#pacman. Outputs T_{B_r}, alpha = dOmega_J/dt, and
	Theta_{K_r} = T_{K_r}/K_r.'''
	J, Kr, Br = sympy.symbols('J Kr Br')
	sys = solve(
		['Ts'],
		["WJ' = TJ/J", "TKr' = Kr*WKr"],
		['TBr = Br*WBr'],
		['TJ = Ts - TKr - TBr', 'WKr = WJ', 'WBr = WJ'],
		['TBr', "WJ'", 'TKr/Kr'])
	check(sys,
		A=[[-Br/J, -1/J], [Kr, 0]],
		B=[[1/J], [0]],
		C=[[Br, 0], [-Br/J, -1/J], [0, 1/Kr]],
		D=[[0], [1/J], [0]])
	check_standard_form(sys)


# --------------------------------------------------------------------------
# Chapter 3, normal-tree-to-state-space.md (3.4, hash s0)

def test_3_4_example_circuit_with_voltage_source():
	'''3.4 normal-tree-to-state-space.md, ex:state_model_ex_01: RC-RL circuit
	with outputs i_L, i_s, v_{R_2}.'''
	R1, R2, L, C = sympy.symbols('R1 R2 L C')
	sys = solve(
		['Vs'],
		["vC' = iC/C", "iL' = vL/L"],
		['iR1 = vR1/R1', 'vR2 = R2*iR2'],
		['iC = iR1 - iL', 'iR2 = iL', 'vL = vC - vR2', 'vR1 = Vs - vC',
		 'iS = iR1'],  # 2d: contour around the source's + node
		['iL', 'iS', 'vR2'])
	check(sys,
		A=[[-1/(R1*C), -1/C], [1/L, -R2/L]],
		B=[[1/(R1*C)], [0]],
		C=[[0, 1], [-1/R1, 0], [0, R2]],
		D=[[0], [1/R1], [0]])
	check_standard_form(sys)


def test_3_4_example_loudspeaker_crossover():
	'''3.4 normal-tree-to-state-space.md, ex:crossover-state-model: crossover
	with outputs v_{R_t} (tweeter) and v_{R_w} (woofer).'''
	Rt, RL, Rw, L, C = sympy.symbols('Rt RL Rw L C')
	sys = solve(
		['Vs'],
		["vC' = iC/C", "iL' = vL/L"],
		['iRt = vRt/Rt', 'vRL = RL*iRL', 'vRw = Rw*iRw'],
		['iC = iRt', 'iRL = iL', 'iRw = iL',
		 'vRt = Vs - vC', 'vL = Vs - vRL - vRw'],
		['vRt', 'vRw'])
	check(sys,
		A=[[-1/(Rt*C), 0], [0, -(RL + Rw)/L]],
		B=[[1/(Rt*C)], [1/L]],
		C=[[-1, 0], [0, Rw]],
		D=[[1], [0]])
	check_standard_form(sys)


# --------------------------------------------------------------------------
# Chapter 3, state-space-model-of-a-translational-mechanical-system.md (3.5, d7)

def test_3_5_two_mass_chain():
	'''3.5 state-space-model-of-a-translational-mechanical-system.md,
	ex:state_model_ex_02: two masses in a chain driven by V_s; outputs the
	spring forces and the momenta p_{m_i} = m_i v_{m_i}.'''
	m1, m2, K1, K2, B1, B2 = sympy.symbols('m1 m2 K1 K2 B1 B2')
	sys = solve(
		['Vs'],
		["vm1' = Fm1/m1", "vm2' = Fm2/m2", "FK1' = K1*vK1", "FK2' = K2*vK2"],
		['FB1 = B1*vB1', 'FB2 = B2*vB2'],
		['Fm1 = -FK1 - FB1 + FK2 + FB2', 'Fm2 = -FK2 - FB2',
		 'vK1 = vm1 - Vs', 'vB1 = vm1 - Vs',
		 'vK2 = vm2 - vm1', 'vB2 = vm2 - vm1'],
		['FK1', 'FK2', 'm1*vm1', 'm2*vm2'])
	check(sys,
		A=[[-(B1 + B2)/m1, B2/m1, -1/m1, 1/m1],
		   [B2/m2, -B2/m2, 0, -1/m2],
		   [K1, 0, 0, 0],
		   [-K2, K2, 0, 0]],
		B=[[B1/m1], [0], [-K1], [0]],
		C=[[0, 0, 1, 0], [0, 0, 0, 1], [m1, 0, 0, 0], [0, m2, 0, 0]],
		D=sympy.zeros(4, 1))
	check_standard_form(sys)


# --------------------------------------------------------------------------
# Chapter 3, state-space-model-of-a-rotational-mechanical-system.md (3.6, zs)

def test_3_6_drag_cup_drive():
	'''3.6 state-space-model-of-a-rotational-mechanical-system.md,
	ex:state_model_ex_03: Omega_s drives J through a drag cup B_1; bearing
	B_2; spring K_r to a wall. Outputs T_{K_r}, h_J = J Omega_J, and the
	torque the source delivers, T_{Omega_s} (TWs).'''
	J, Kr, B1, B2 = sympy.symbols('J Kr B1 B2')
	sys = solve(
		['Ws'],
		["WJ' = TJ/J", "TKr' = Kr*WKr"],
		['TB1 = B1*WB1', 'TB2 = B2*WB2'],
		['TJ = TKr - TB1 - TB2', 'WB1 = WJ - Ws', 'WB2 = WJ', 'WKr = -WJ',
		 'TWs = -TB1'],  # 2d: continuity at node A
		['TKr', 'J*WJ', 'TWs'])
	check(sys,
		A=[[-(B1 + B2)/J, 1/J], [-Kr, 0]],
		B=[[B1/J], [0]],
		C=[[0, 1], [J, 0], [-B1, 0]],
		D=[[0], [0], [B1]])
	check_standard_form(sys)


def test_3_6_ceiling_fan():
	'''3.6 state-space-model-of-a-rotational-mechanical-system.md,
	ex:ceiling-fan-state-model: rotor J_1, rubber flywheel K_r, blades J_2,
	linear drag B_2. Outputs Omega_{J_2} and T_{K_r}.'''
	J1, J2, Kr, B1, B2 = sympy.symbols('J1 J2 Kr B1 B2')
	sys = solve(
		['Ts'],
		["WJ1' = TJ1/J1", "WJ2' = TJ2/J2", "TKr' = Kr*WKr"],
		['TB1 = B1*WB1', 'TB2 = B2*WB2'],
		['TJ1 = Ts - TB1 + TKr', 'TJ2 = -TKr - TB2',
		 'WB1 = WJ1', 'WB2 = WJ2', 'WKr = WJ2 - WJ1'],
		['WJ2', 'TKr'])
	check(sys,
		A=[[-B1/J1, 0, 1/J1], [0, -B2/J2, -1/J2], [-Kr, Kr, 0]],
		B=[[1/J1], [0], [0]],
		C=[[0, 1, 0], [0, 0, 1]],
		D=[[0], [0]])
	check_standard_form(sys)


def test_3_6_ceiling_fan_quadratic_drag():
	'''3.6 state-space-model-of-a-rotational-mechanical-system.md, end of
	ex:ceiling-fan-state-model: with T_{B_2} = c|Omega_{J_2}|Omega_{J_2} "the
	same steps give a nonlinear state equation". The notes do not print it;
	the expected f(x, u) is the linear one with B_2 Omega_{J_2} replaced.'''
	J1, J2, Kr, B1, c = sympy.symbols('J1 J2 Kr B1 c')
	WJ1, WJ2, TKr, Ts = sympy.symbols('WJ1 WJ2 TKr Ts')
	sys = solve(
		['Ts'],
		["WJ1' = TJ1/J1", "WJ2' = TJ2/J2", "TKr' = Kr*WKr"],
		['TB1 = B1*WB1', 'TB2 = c*Abs(WB2)*WB2'],
		['TJ1 = Ts - TB1 + TKr', 'TJ2 = -TKr - TB2',
		 'WB1 = WJ1', 'WB2 = WJ2', 'WKr = WJ2 - WJ1'],
		['WJ2', 'TKr'])
	assert_matrix('StateEq', sys.StateEq, [
		[(Ts - B1*WJ1 + TKr)/J1],
		[(-TKr - c*sympy.Abs(WJ2)*WJ2)/J2],
		[Kr*(WJ2 - WJ1)]])


# --------------------------------------------------------------------------
# Chapter 3, nonstandard-state-equations.md (3.7, hash nq)

def test_3_7_ac_coupling_input_derivative():
	'''3.7 nonstandard-state-equations.md, ex:ac-coupling-state and part 2 of
	ex:matrix-reduction: AC-coupled amplifier input; the dependent capacitor
	C_1 brings in dV_s/dt. Checks A, B, E and the transformed B' = AE + B,
	D' = CE + D for the output v_{C_2}.'''
	R, C1, C2 = sympy.symbols('R C1 C2')
	sys = solve(
		['Vs'],
		["vC2' = iC2/C2"],
		['iR = vR/R', "iC1 = C1*vC1'"],
		['iC2 = iC1 - iR', 'vC1 = Vs - vC2', 'vR = vC2'],
		['vC2'])
	check(sys,
		A=[[-1/(R*(C1 + C2))]],
		B=[[0]],
		E=[[C1/(C1 + C2)]],
		C=[[1]],
		D=[[0]],
		F=[[0]],
		Bp=[[-C1/(R*(C1 + C2)**2)]],
		Dp=[[C1/(C1 + C2)]])


def test_3_7_solenoid_coupled_resistors():
	'''3.7 nonstandard-state-equations.md, ex:solenoid-coupled and part 1 of
	ex:matrix-reduction: coil L fed through R_1 with R_2 across it; the
	resistors' equations are coupled. Outputs v_{R_1} and i_{R_2}, whose rows
	are the notes' H' (C) and L' (D).'''
	R1, R2, L = sympy.symbols('R1 R2 L')
	sys = solve(
		['Vs'],
		["iL' = vL/L"],
		['vR1 = R1*iR1', 'iR2 = vR2/R2'],
		['iR1 = iR2 + iL', 'vR2 = Vs - vR1', 'vL = Vs - vR1'],
		['vR1', 'iR2'])
	check(sys,
		A=[[-R1*R2/((R1 + R2)*L)]],
		B=[[R2/((R1 + R2)*L)]],
		C=[[R1*R2/(R1 + R2)], [-R1/(R1 + R2)]],
		D=[[R1/(R1 + R2)], [1/(R1 + R2)]])
	check_standard_form(sys)


# --------------------------------------------------------------------------
# Chapter 3, worked-examples.md (3.8, hash we)

def test_3_8_truck_seat_suspension():
	'''3.8 worked-examples.md, ex:seat-suspension: seat m on spring K and
	damper B, floor velocity V_s. Outputs dv_m/dt and x_K = F_K/K.'''
	m, K, B = sympy.symbols('m K B')
	sys = solve(
		['Vs'],
		["vm' = Fm/m", "FK' = K*vK"],
		['FB = B*vB'],
		['Fm = -FK - FB', 'vK = vm - Vs', 'vB = vm - Vs'],
		["vm'", 'FK/K'])
	check(sys,
		A=[[-B/m, -1/m], [K, 0]],
		B=[[B/m], [-K]],
		C=[[-B/m, -1/m], [0, 1/K]],
		D=[[B/m], [0]])
	check_standard_form(sys)


def test_3_8_guitar_pickup():
	'''3.8 worked-examples.md, ex:guitar-pickup: pickup R_p, L; cable C;
	amplifier R_a. Output v_a = v_{R_a}.'''
	Rp, Ra, L, C = sympy.symbols('Rp Ra L C')
	sys = solve(
		['Vs'],
		["vC' = iC/C", "iL' = vL/L"],
		['vRp = Rp*iRp', 'iRa = vRa/Ra'],
		['iRp = iL', 'iC = iL - iRa', 'vL = Vs - vRp - vC', 'vRa = vC'],
		['vRa'])
	check(sys,
		A=[[-1/(Ra*C), 1/C], [-1/L, -Rp/L]],
		B=[[0], [1/L]],
		C=[[1, 0]],
		D=[[0]])
	check_standard_form(sys)


def test_3_8_car_trailer():
	'''3.8 worked-examples.md, ex:car-trailer: car m_1 tows trailer m_2
	through hitch K, B; drags B_1, B_2. Output the hitch force F_K + F_B.'''
	m1, m2, K, B, B1, B2 = sympy.symbols('m1 m2 K B B1 B2')
	sys = solve(
		['Fs'],
		["vm1' = Fm1/m1", "vm2' = Fm2/m2", "FK' = K*vK"],
		['FB = B*vB', 'FB1 = B1*vB1', 'FB2 = B2*vB2'],
		['Fm1 = Fs - FB1 - FK - FB', 'Fm2 = FK + FB - FB2',
		 'vB1 = vm1', 'vB2 = vm2', 'vK = vm1 - vm2', 'vB = vm1 - vm2'],
		['FK + FB'])
	check(sys,
		A=[[-(B1 + B)/m1, B/m1, -1/m1],
		   [B/m2, -(B + B2)/m2, 1/m2],
		   [K, -K, 0]],
		B=[[1/m1], [0], [0]],
		C=[[B, -B, 1]],
		D=[[0]])
	check_standard_form(sys)


def test_3_8_bulk_capacitor_ideal_supply():
	'''3.8 worked-examples.md, ex:bulk-capacitor part 1: ideal V_s across a
	dependent capacitor C and a winding R_w, L. Output i_s = i_L + i_C, so
	F = C.'''
	Rw, L, C = sympy.symbols('Rw L C')
	sys = solve(
		['Vs'],
		["iL' = vL/L"],
		['vRw = Rw*iRw', "iC = C*vC'"],
		['iRw = iL', 'vL = Vs - vRw', 'vC = Vs',
		 'iS = iL + iC'],  # contour around node A
		['iS'])
	check(sys,
		A=[[-Rw/L]],
		B=[[1/L]],
		E=[[0]],
		C=[[1]],
		D=[[0]],
		F=[[C]])


def test_3_8_bulk_capacitor_supply_resistance():
	'''3.8 worked-examples.md, ex:bulk-capacitor part 2: supply resistance R_s
	makes C independent; the circuit is 3.4's first example with R_1 = R_s,
	R_2 = R_w. Output i_s.'''
	Rs, Rw, L, C = sympy.symbols('Rs Rw L C')
	sys = solve(
		['Vs'],
		["vC' = iC/C", "iL' = vL/L"],
		['iRs = vRs/Rs', 'vRw = Rw*iRw'],
		['iC = iRs - iL', 'iRw = iL', 'vL = vC - vRw', 'vRs = Vs - vC',
		 'iS = iRs'],
		['iS'])
	check(sys,
		A=[[-1/(Rs*C), -1/C], [1/L, -Rw/L]],
		B=[[1/(Rs*C)], [0]],
		C=[[-1/Rs, 0]],
		D=[[1/Rs]])
	check_standard_form(sys)


# --------------------------------------------------------------------------
# Chapter 3, state-space-models/problems.md (hash k8)

def test_3_problems_nintendo():
	'''Ch. 3 problems.md#nintendo: series RLC with V_s; outputs i_R, v_C.'''
	R, L, C = sympy.symbols('R L C')
	sys = solve(
		['Vs'],
		["vC' = iC/C", "iL' = vL/L"],
		['vR = iR*R'],
		['iR = iL', 'iC = iL', 'vL = -vR + Vs - vC'],
		['iR', 'vC'])
	check(sys,
		A=[[0, 1/C], [-1/L, -R/L]],
		B=[[0], [1/L]],
		C=[[0, 1], [1, 0]],
		D=[[0], [0]])
	check_standard_form(sys)


def test_3_problems_supernintendo():
	'''Ch. 3 problems.md#supernintendo: mass and spring with F_s; no D-type
	elements, so the other elemental equations are an empty list.'''
	m, K = sympy.symbols('m K')
	sys = solve(
		['Fs'],
		["vm' = Fm/m", "FK' = K*vK"],
		[],
		['Fm = Fs - FK', 'vK = vm'],
		['vm', 'FK'])
	check(sys,
		A=[[0, -1/m], [K, 0]],
		B=[[1/m], [0]],
		C=[[1, 0], [0, 1]],
		D=[[0], [0]])
	check_standard_form(sys)


def test_3_problems_gameboy():
	'''Ch. 3 problems.md#gameboy: J, K_r, B_r with T_s; outputs Omega_J,
	T_{B_r}.'''
	J, Kr, Br = sympy.symbols('J Kr Br')
	sys = solve(
		['Ts'],
		["WJ' = TJ/J", "TKr' = Kr*WKr"],
		['TBr = Br*WBr'],
		['TJ = Ts - TKr - TBr', 'WKr = WJ', 'WBr = WJ'],
		['WJ', 'TBr'])
	check(sys,
		A=[[-Br/J, -1/J], [Kr, 0]],
		B=[[1/J], [0]],
		C=[[1, 0], [Br, 0]],
		D=[[0], [0]])
	check_standard_form(sys)


def test_3_problems_blowhard():
	'''Ch. 3 problems.md#blowhard: Omega_s drives J through B_r and K_r in
	series; outputs Omega_J and Theta_{K_r} = T_{K_r}/K_r.'''
	J, Kr, Br = sympy.symbols('J Kr Br')
	sys = solve(
		['Ws'],
		["WJ' = TJ/J", "TKr' = Kr*WKr"],
		['WBr = TBr/Br'],
		['TBr = TKr', 'TJ = TKr', 'WKr = -WBr + Ws - WJ'],
		['WJ', 'TKr/Kr'])
	check(sys,
		A=[[0, 1/J], [-Kr, -Kr/Br]],
		B=[[0], [Kr]],
		C=[[1, 0], [0, 1/Kr]],
		D=[[0], [0]])
	check_standard_form(sys)


def test_3_problems_blinken():
	'''Ch. 3 problems.md#blinken: I_s into C parallel R; outputs v_C, i_R.

	NOTES ERRATUM: the solution writes R's elemental equation as
	"v_R = i_R R" (problems.md:696), though it names i_R a primary variable
	and v_R = v_C a compatibility equation, so R is a link and its equation
	solved for the primary variable is i_R = v_R/R, used here.'''
	R, C = sympy.symbols('R C')
	sys = solve(
		['Is'],
		["vC' = iC/C"],
		['iR = vR/R'],
		['iC = Is - iR', 'vR = vC'],
		['vC', 'iR'])
	check(sys,
		A=[[-1/(R*C)]],
		B=[[1/C]],
		C=[[1], [1/R]],
		D=[[0], [0]])
	check_standard_form(sys)


def test_3_problems_valencia():
	'''Ch. 3 problems.md#valencia: two masses, spring K, damper B to ground,
	force F_s; outputs v_{m_1}, v_{m_2}.'''
	m1, m2, K, B = sympy.symbols('m1 m2 K B')
	sys = solve(
		['Fs'],
		["vm1' = Fm1/m1", "vm2' = Fm2/m2", "FK' = K*vK"],
		['FB = B*vB'],
		['Fm1 = Fs - FK', 'Fm2 = FK - FB', 'vK = vm1 - vm2', 'vB = vm2'],
		['vm1', 'vm2'])
	check(sys,
		A=[[0, 0, -1/m1], [0, -B/m2, 1/m2], [K, -K, 0]],
		B=[[1/m1], [0], [0]],
		C=[[1, 0, 0], [0, 1, 0]],
		D=[[0], [0]])
	check_standard_form(sys)


def test_3_problems_stevenash():
	'''Ch. 3 problems.md#stevenash: V_s, R, C_1, L, C_2; outputs v_{C_2},
	v_R, and the source current i_s = i_R.'''
	R, L, C1, C2 = sympy.symbols('R L C1 C2')
	sys = solve(
		['Vs'],
		["vC1' = iC1/C1", "vC2' = iC2/C2", "iL' = vL/L"],
		['iR = vR/R'],
		['iC1 = iR - iL', 'iC2 = iL', 'vL = vC1 - vC2', 'vR = Vs - vC1',
		 'iS = iR'],  # 4: the source's + node touches only R
		['vC2', 'vR', 'iS'])
	check(sys,
		A=[[-1/(R*C1), 0, -1/C1], [0, 0, 1/C2], [1/L, -1/L, 0]],
		B=[[1/(R*C1)], [0], [0]],
		C=[[0, 1, 0], [-1, 0, 0], [-1/R, 0, 0]],
		D=[[0], [1], [1/R]])
	check_standard_form(sys)


def test_3_problems_tetris():
	'''Ch. 3 problems.md#tetris: T_s drives flywheel J through a dependent
	coupling K_r; bearing B_r. Output Omega_1 = Omega_J - Omega_{K_r}, which
	has F = 1/K_r.'''
	J, Kr, Br = sympy.symbols('J Kr Br')
	sys = solve(
		['Ts'],
		["WJ' = TJ/J"],
		['TBr = Br*WBr', "WKr = TKr'/Kr"],
		['TJ = Ts - TBr', 'TKr = -Ts', 'WBr = WJ'],
		['WJ - WKr'])
	check(sys,
		A=[[-Br/J]],
		B=[[1/J]],
		E=[[0]],
		C=[[1]],
		D=[[0]],
		F=[[1/Kr]])


def test_3_problems_galaga():
	'''Ch. 3 problems.md#galaga: Omega_s drives J through couplings B_1, B_2
	in series (coupled D-type equations). Output T_{B_2} =
	B_e (Omega_J - Omega_s), B_e = B_1 B_2/(B_1 + B_2).'''
	J, B1, B2 = sympy.symbols('J B1 B2')
	Be = B1*B2/(B1 + B2)
	sys = solve(
		['Ws'],
		["WJ' = TJ/J"],
		['WB1 = TB1/B1', 'TB2 = B2*WB2'],
		['TJ = -TB2', 'TB1 = TB2', 'WB2 = WJ - Ws - WB1'],
		['TB2'])
	check(sys,
		A=[[-Be/J]],
		B=[[Be/J]],
		C=[[Be]],
		D=[[-Be]])
	check_standard_form(sys)


def test_3_problems_donkeykong():
	'''Ch. 3 problems.md#donkeykong: divider R_1, R_2 feeding C through R_3
	(three coupled D-type equations). Output i_{R_3}, whose row is the
	notes' third rows of H' and L'.'''
	R1, R2, R3, C = sympy.symbols('R1 R2 R3 C')
	Delta = R1*R2 + R1*R3 + R2*R3
	sys = solve(
		['Vs'],
		["vC' = iC/C"],
		['vR1 = R1*iR1', 'iR2 = vR2/R2', 'iR3 = vR3/R3'],
		['iC = iR3', 'iR1 = iR2 + iR3',
		 'vR2 = Vs - vR1', 'vR3 = Vs - vR1 - vC'],
		['iR3'])
	check(sys,
		A=[[-(R1 + R2)/(Delta*C)]],
		B=[[R2/(Delta*C)]],
		C=[[-(R1 + R2)/Delta]],
		D=[[R2/Delta]])
	check_standard_form(sys)


# --------------------------------------------------------------------------
# Chapter 4, electromechanical-systems/
#
# The four models below that the notes solved with the StateMint web
# interface are run from the .rnd files the notes link (copied, with their
# EXIF UserComment JSON, into tests/data/). The fields are reproduced
# verbatim; split_field splits them the way the web interface does.

RND_MOTOR_MODEL = {  # tests/data/motor_model.rnd
	'InVars': 'Vs',
	'StVarElEqns': "OJ' = 1/J*TJ, iL' = 1/L*vL",
	'OtherElEqns': 'TB = B*OB, vR = iR*R, v1 = TF*O2, T2 = -TF*i1',
	'Constraints': 'iR = iL, i1 = iL, TJ = -T2 - TB, vL = -vR + Vs - v1, '
		'O2 = OJ, OB = OJ',
	'OutputVars': 'OJ,TJ,vL,iL,OB,TB,vR,iR,v1,i1,O2,T2,Vs,iR',
}

RND_MOTOR_MODEL_CHARACTERISTICS = {  # tests/data/motor_model_characteristics.rnd
	'InVars': 'Vs, Ts',
	'StVarElEqns': "OJ' = 1/J*TJ, iL' = 1/L*vL",
	'OtherElEqns': 'TB = B*OB, vR = iR*R, v1 = TF*O2, T2 = -TF*i1',
	'Constraints': 'iR = iL, i1 = iL, TJ = -T2 - TB - Ts, '
		'vL = -vR + Vs - v1, O2 = OJ, OB = OJ',
	'OutputVars': 'OJ,TJ,vL,iL,OB,TB,vR,iR,v1,i1,O2,T2,Vs,iR',
}

RND_QUADRILATERAL = {  # tests/data/quadrilateral.rnd
	'InVars': 'VS',
	'StVarElEqns': "OJm' = 1/Jm * TJm,\nOJf' = 1/Jf * TJf,\n"
		"iL' = 1/L * vL,\nTk' = k * Ok",
	'OtherElEqns': 'TBm = Bm * OBm,\nTBb = Bb * OBb,\nvR = iR * R,\n'
		'T2 = -Ka * i1,\nv1 = Ka * O2',
	'Constraints': 'TJm = -T2 - TBm - Tk,\nTJf = Tk - TBb,\n'
		'vL = -vR + VS - v1,\nOk = OJm - OJf,\nOBm = OJm,\nOBb = OJm,\n'
		'iR = iL,\ni1 = iL,\nO2 = OJm',
	'OutputVars': 'i1, OJf',
}

RND_MRPOTATOHEAD = {  # tests/data/mrpotatohead.rnd
	'InVars': 'VS',
	'StVarElEqns': "OJ4' = 1/J4 * TJ4,\niL' = 1/L * vL",
	'OtherElEqns': "TJ2 = J2 * OJ2',\nTB2 = B2 * OB2,\nTB4 = B4 * OB4,\n"
		'vR = iR * R,\nT2 = -Ka * i1,\nv1 = Ka * O2,\nT4 = -N * T3,\n'
		'O3 = N * O4',
	'Constraints': 'TJ4 = -T4 - TB4,\nvL = -vR + VS - v1,\nOJ2 = O3,\n'
		'OB2 = O3,\nOB4 = OJ4,\niR = iL,\ni1 = iL,\nO2 = O3,\n'
		'T3 = -TJ2 - TB2 - T2,\nO4 = OJ4',
	'OutputVars': 'OJ2, OJ4',
}

# The .rnd names: O for Omega, B for B_r (B_rm in dc-motor-performance), and
# iR for the source current I_s (the last output).
_MOTOR_C = [
	[1, 0],    # Omega_J
	['-B', 'TF'],  # T_J
	['-TF', '-R'],  # v_L
	[0, 1],    # i_L
	[1, 0],    # Omega_B
	['B', 0],  # T_B
	[0, 'R'],  # v_R
	[0, 1],    # i_R
	['TF', 0],  # v_1
	[0, 1],    # i_1
	[1, 0],    # Omega_2
	[0, '-TF'],  # T_2
	[0, 0],    # V_s
	[0, 1],    # I_s
]


def _motor_C():
	B, TF, R = sympy.symbols('B TF R')
	env = {'B': B, 'TF': TF, 'R': R}
	return sympy.Matrix([[sympy.sympify(e, locals=env) for e in row]
		for row in _MOTOR_C])


def test_4_4_real_motor_model_rnd():
	'''4.4 modeling-a-real-electromechanical-system.md (sub:motor_linear_
	graph_model), motor_model.rnd (footnote 8): V_s drives a DC motor
	(R, L, transducer TF) turning J against B_r. All 14 variables out.'''
	J, L, B, R, TF = sympy.symbols('J L B R TF')
	sys = solve_rnd(RND_MOTOR_MODEL)
	D = sympy.zeros(14, 1)
	D[2, 0] = 1   # v_L
	D[12, 0] = 1  # V_s
	check(sys,
		A=[[-B/J, TF/J], [-TF/L, -R/L]],
		B=[[0], [1/L]],
		C=_motor_C(),
		D=D)
	check_standard_form(sys)


def test_4_5_motor_test_configuration_rnd():
	'''4.5 dc-motor-performance-in-steady-state.md (sec:modeling_test_
	system), motor_model_characteristics.rnd (footnote 10): the motor with a
	brake torque T_s on the shaft; inputs V_s, T_s.'''
	J, L, B, R, TF = sympy.symbols('J L B R TF')
	sys = solve_rnd(RND_MOTOR_MODEL_CHARACTERISTICS)
	D = sympy.zeros(14, 2)
	D[2, 0] = 1    # v_L
	D[12, 0] = 1   # V_s
	D[1, 1] = -1   # T_J
	check(sys,
		A=[[-B/J, TF/J], [-TF/L, -R/L]],
		B=[[0, -1/J], [1/L, 0]],
		C=_motor_C(),
		D=D)
	check_standard_form(sys)


def test_4_problems_quadrilateral_rnd():
	'''Ch. 4 problems.md#quadrilateral, quadrilateral.rnd: motor (R, L, K_a)
	with rotor J_m, damping B_rm, flexible coupling K_r (Tk), flywheel J_f
	with bearing B_rb. x = [Omega_Jm, Omega_Jf, i_L, T_Kr]; outputs i_1,
	Omega_Jf. Checks StateMint reproduces what the notes print from it.

	NOTES ERRATUM: the .rnd has "OBb = OJm", but the notes' table says
	Omega_{B_rb} = Omega_{J_f}. The notes' A (problems.md:350) and its
	MATLAB listing were produced from the .rnd, so their row 2 is
	[-B_rb/J_f, 0, 0, 1/J_f]. See test_4_problems_quadrilateral_table for
	the model the table describes.'''
	Jm, Jf, L, k, Bm, Bb, R, Ka = sympy.symbols('Jm Jf L k Bm Bb R Ka')
	sys = solve_rnd(RND_QUADRILATERAL)
	check(sys,
		A=[[-Bm/Jm, 0, Ka/Jm, -1/Jm],
		   [-Bb/Jf, 0, 0, 1/Jf],
		   [-Ka/L, 0, -R/L, 0],
		   [k, -k, 0, 0]],
		B=[[0], [0], [1/L], [0]],
		C=[[0, 0, 1, 0], [0, 1, 0, 0]],
		D=[[0], [0]])
	check_standard_form(sys)


def test_4_problems_quadrilateral_table():
	'''Ch. 4 problems.md#quadrilateral, from the notes' equation table
	(problems.md:331-339) rather than the .rnd: the bearing B_rb turns with
	the flywheel, Omega_{B_rb} = Omega_{J_f}.

	NOTES ERRATUM: A's row 2 should be [0, -B_rb/J_f, 0, 1/J_f], not
	[-B_rb/J_f, 0, 0, 1/J_f] as printed (problems.md:350 and the MATLAB
	listing). The table writes element 2's equation as Omega_2 = v_1/K_a;
	solved for its primary variable it is v_1 = K_a Omega_2, used here.'''
	Jm, Jf, L, Kr, Brm, Brb, R, Ka = sympy.symbols('Jm Jf L Kr Brm Brb R Ka')
	sys = solve(
		['Vs'],
		["WJm' = TJm/Jm", "WJf' = TJf/Jf", "iL' = vL/L", "TKr' = Kr*WKr"],
		['TBrm = Brm*WBrm', 'TBrb = Brb*WBrb', 'vR = iR*R',
		 'T2 = -Ka*i1', 'v1 = Ka*W2'],
		['TJm = -T2 - TBrm - TKr', 'TJf = TKr - TBrb',
		 'vL = -vR + Vs - v1', 'WKr = WJm - WJf', 'WBrm = WJm',
		 'WBrb = WJf', 'iR = iL', 'i1 = iL', 'W2 = WJm'],
		['i1', 'WJf'])
	check(sys,
		A=[[-Brm/Jm, 0, Ka/Jm, -1/Jm],
		   [0, -Brb/Jf, 0, 1/Jf],
		   [-Ka/L, 0, -R/L, 0],
		   [Kr, -Kr, 0, 0]],
		B=[[0], [0], [1/L], [0]],
		C=[[0, 0, 1, 0], [0, 1, 0, 0]],
		D=[[0], [0]])
	check_standard_form(sys)


def test_4_problems_mrpotatohead_rnd():
	'''Ch. 4 problems.md#mrpotatohead, mrpotatohead.rnd: motor (R, L, K_a)
	with dependent rotor inertia J_2 and damping B_r2, gear pair N, load J_4
	with damping B_r4. x = [Omega_J4, i_L]; outputs Omega_J2, Omega_J4.'''
	J2, J4, B2, B4, L, R, Ka, N = sympy.symbols('J2 J4 B2 B4 L R Ka N')
	sys = solve_rnd(RND_MRPOTATOHEAD)
	check(sys,
		A=[[-(B2*N**2 + B4)/(J2*N**2 + J4), Ka*N/(J2*N**2 + J4)],
		   [-Ka*N/L, -R/L]],
		B=[[0], [1/L]],
		C=[[N, 0], [1, 0]],
		D=[[0], [0]])
	check_standard_form(sys)


def test_4_problems_rectangle():
	'''Ch. 4 problems.md#rectangle: I_s drives a motor (dependent L, R, K_a)
	turning J_1, coupled by K_r1 to J_2, which K_r2 ties to ground; bearings
	B_r1, B_r2. x = [Omega_J1, T_Kr1, Omega_J2, T_Kr2]; outputs Theta_J1 =
	T_Kr1/K_r1 + T_Kr2/K_r2 and Theta_J2 = T_Kr2/K_r2.

	NOTES ERRATUM: A[3, 2] is printed 1/J_1 (problems.md:256); it is 1/J_2,
	from the table's dOmega_J2/dt = (T_Kr1 - T_Br2 - T_Kr2)/J_2. The table
	also writes L's equation as di_L/dt = v_L/L, but L is in the tree (i_L =
	I_s), so it is dependent: v_L = L di_L/dt, as the second table has it.
	Element 2's equation Omega_2 = v_1/K_a is used solved for v_1.'''
	J1, J2, Kr1, Kr2, Br1, Br2, Ka, L, R = sympy.symbols(
		'J1 J2 Kr1 Kr2 Br1 Br2 Ka L R')
	sys = solve(
		['Is'],
		["WJ1' = TJ1/J1", "TKr1' = Kr1*WKr1", "WJ2' = TJ2/J2",
		 "TKr2' = Kr2*WKr2"],
		['TBr1 = Br1*WBr1', 'TBr2 = Br2*WBr2', 'T2 = -Ka*i1',
		 'v1 = Ka*W2', "vL = L*iL'", 'vR = iR*R'],
		['TJ1 = -TKr1 - TBr1 - T2', 'WKr1 = WJ1 - WJ2',
		 'TJ2 = TKr1 - TBr2 - TKr2', 'WKr2 = WJ2', 'WBr1 = WJ1',
		 'WBr2 = WJ2', 'i1 = Is', 'W2 = WJ1', 'iL = Is', 'iR = Is'],
		['TKr1/Kr1 + TKr2/Kr2', 'TKr2/Kr2'])
	check(sys,
		A=[[-Br1/J1, -1/J1, 0, 0],
		   [Kr1, 0, -Kr1, 0],
		   [0, 1/J2, -Br2/J2, -1/J2],
		   [0, 0, Kr2, 0]],
		B=[[Ka/J1], [0], [0], [0]],
		C=[[0, 1/Kr1, 0, 1/Kr2], [0, 0, 0, 1/Kr2]],
		D=[[0], [0]])
	check_standard_form(sys)


def test_4_problems_levitation():
	'''Ch. 4 problems.md#levitation: V_s drives a motor (R, L, K_a) turning J,
	which drives B_r and K_r in series. x = [Omega_J, T_Kr, i_L]; outputs
	Omega_J, Omega_Br.

	The table writes B_r's and element 2's equations as T_Br = B_r Omega_Br
	and Omega_2 = v_1/K_a, but B_r is a branch (T_Br = T_Kr) and 2 a link,
	so solved for their primary variables they are Omega_Br = T_Br/B_r and
	v_1 = K_a Omega_2, which the solution's step 4 uses.'''
	J, Kr, Br, L, R, Ka = sympy.symbols('J Kr Br L R Ka')
	sys = solve(
		['Vs'],
		["WJ' = TJ/J", "TKr' = Kr*WKr", "iL' = vL/L"],
		['WBr = TBr/Br', 'vR = iR*R', 'T2 = -Ka*i1', 'v1 = Ka*W2'],
		['TJ = -T2 - TKr', 'WKr = -WBr + WJ', 'vL = -vR + Vs - v1',
		 'TBr = TKr', 'iR = iL', 'i1 = iL', 'W2 = WJ'],
		['WJ', 'WBr'])
	check(sys,
		A=[[0, -1/J, Ka/J], [Kr, -Kr/Br, 0], [-Ka/L, 0, -R/L]],
		B=[[0], [0], [1/L]],
		C=[[1, 0, 0], [0, 1/Br, 0]],
		D=[[0], [0]])
	check_standard_form(sys)


# --------------------------------------------------------------------------
# Chapter 5, linear-time-invariant-system-properties/
# vibration-isolation-table-analysis.md (5.3, hash b9)

def test_5_3_vibration_isolation_table():
	'''5.3 vibration-isolation-table-analysis.md: table m on spring K and damper
	B, floor velocity V_s; output v_m. This section still uses compression
	positive (F_m = F_K + F_B, v_K = V_s - v_m). Also checks the transfer
	function H(s) = ((B/m)s + K/m)/(s^2 + (B/m)s + K/m).'''
	m, K, B, s = sympy.symbols('m K B s')
	sys = solve(
		['Vs'],
		["vm' = Fm/m", "FK' = K*vK"],
		['FB = B*vB'],
		['Fm = FK + FB', 'vK = Vs - vm', 'vB = Vs - vm'],
		['vm'])
	check(sys,
		A=[[-B/m, 1/m], [-K, 0]],
		B=[[B/m], [K]],
		C=[[1, 0]],
		D=[[0]])
	check_standard_form(sys)
	TF = sympy.Matrix(sys.TF).subs(sympy.Symbol('s'), s)
	assert_matrix('TF', TF,
		[[((B/m)*s + K/m)/(s**2 + (B/m)*s + K/m)]])


# --------------------------------------------------------------------------
# Chapter 8, lumped-parameter-modeling-fluid-and-thermal-systems/

@pytest.mark.parametrize('In', ['Ii', 'I'])  # 2.1.1 read I as sqrt(-1)
def test_8_4_hydroelectric_dam(In):
	'''8.4 state-space-model-of-a-hydroelectric-dam.md: reservoir C_f1,
	pipe R_f1 and inertance I, head sources P_s1, P_s2, turbine (1, 2, alpha),
	tailwater R_f2, C_f2; shaft J, B_r; generator (3, 4, k_m) into R_3, L_2,
	C_3, R_4. x = [P_Cf1, P_Cf2, Q_I, Omega_J, i_L2, v_C3], u = [Q_s, P_s1,
	P_s2]. The notes call the inertance I; the test runs it both as I and as
	Ii.

	NOTES ERRATUM: the section's continuity/compatibility table (lines 76-82)
	lost two of its three columns in conversion from LaTeX: only B_r, 3, 4,
	R_3, R_4 remain, with a stray "\\end{tabular} }". The ten missing
	equations (C_f1, C_f2, I, J, L_2, C_3, R_f1, R_f2, 1, 2) are restored
	here from the original (systems/ch_thermoflu.tex) and agree with the
	figure. Three elemental equations are not solved for their primary
	variables: B_r (a link) is T_Br = B_r Omega_Br, element 2 (a link with 1
	a branch) gives P_1 = alpha Omega_2, and element 3 (a link) T_3 =
	-k_m i_4; those forms are used here.'''
	Cf1, Cf2, Rf1, Rf2, alpha, J, Br, km, R3, L2, C3, R4 = sympy.symbols(
		'Cf1 Cf2 Rf1 Rf2 alpha J Br km R3 L2 C3 R4')
	I = sympy.Symbol(In)
	sys = solve(
		['Qs', 'Ps1', 'Ps2'],
		["PCf1' = QCf1/Cf1", "PCf2' = QCf2/Cf2",
		 "QI' = PI/{}".format(In), "WJ' = TJ/J",
		 "iL2' = vL2/L2", "vC3' = iC3/C3"],
		['PRf1 = QRf1*Rf1', 'PRf2 = QRf2*Rf2',
		 'T2 = -alpha*Q1', 'P1 = alpha*W2',
		 'TBr = Br*WBr', 'T3 = -km*i4', 'v4 = km*W3',
		 'vR3 = iR3*R3', 'iR4 = vR4/R4'],
		['QCf1 = Qs - QI', 'QCf2 = QI',
		 'PI = -PRf1 + PCf1 - PCf2 - PRf2 + Ps2 - P1 + Ps1',
		 'TJ = -T2 - TBr - T3', 'vL2 = -vR3 + v4 - vC3',
		 'iC3 = iL2 - iR4', 'QRf1 = QI', 'QRf2 = QI', 'Q1 = QI', 'W2 = WJ',
		 'WBr = WJ', 'W3 = WJ', 'i4 = -iL2', 'iR3 = iL2', 'vR4 = vC3'],
		['PCf1', 'PCf2', 'QI', 'WJ', 'iL2', 'vC3'])
	check(sys,
		A=[[0, 0, -1/Cf1, 0, 0, 0],
		   [0, 0, 1/Cf2, 0, 0, 0],
		   [1/I, -1/I, -(Rf1 + Rf2)/I, -alpha/I, 0, 0],
		   [0, 0, alpha/J, -Br/J, -km/J, 0],
		   [0, 0, 0, km/L2, -R3/L2, -1/L2],
		   [0, 0, 0, 0, 1/C3, -1/(R4*C3)]],
		B=[[1/Cf1, 0, 0],
		   [0, 0, 0],
		   [0, 1/I, 1/I],
		   [0, 0, 0],
		   [0, 0, 0],
		   [0, 0, 0]])
	check_standard_form(sys)


def test_8_5_thermal_finite_element_bar():
	'''8.5 thermal-finite-element-model.md: an insulated bar in n sections,
	R_t and C_t each, driven by T_s at one end; y = x. Checked for n = 5
	with tau = R_t C_t.'''
	n = 5
	Rt, Ct = sympy.symbols('Rt Ct')
	tau = Rt*Ct
	st = ["TC{0}' = qC{0}/Ct".format(i) for i in range(1, n + 1)]
	other = ['qR{0} = TR{0}/Rt'.format(i) for i in range(1, n + 1)]
	cons = ['qC{0} = qR{0} - qR{1}'.format(i, i + 1) for i in range(1, n)]
	cons += ['qC{0} = qR{0}'.format(n), 'TR1 = Ts - TC1']
	cons += ['TR{0} = TC{1} - TC{0}'.format(i, i - 1)
		for i in range(2, n + 1)]
	sys = solve(['Ts'], st, other, cons,
		['TC{}'.format(i) for i in range(1, n + 1)])
	A = sympy.zeros(n, n)
	for i in range(n):
		A[i, i] = -2/tau
		if i > 0:
			A[i, i - 1] = 1/tau
		if i < n - 1:
			A[i, i + 1] = 1/tau
	A[n - 1, n - 1] = -1/tau
	B = sympy.zeros(n, 1)
	B[0, 0] = 1/tau
	check(sys, A=A, B=B, C=sympy.eye(n), D=sympy.zeros(n, 1))
	check_standard_form(sys)


# --------------------------------------------------------------------------
# Chapter 14, nonlinear-systems-and-linearization/
# For a nonlinear model StateMint's A and B are the Jacobians of f(x, u);
# evaluated at the operating point they are the linearized model's.

def test_14_5_nonlinear_fluid_overflow():
	'''14.5 nonlinear-systems-and-linearization/nonlinear-fluid-system-example.md
	(hash t0): Q_s fills C, drained by a pipe of inertance L and nonlinear
	resistance R(P_C) = R_inf + (R_0 - R_inf)/2 (1 - tanh(5 (P_C -
	Pbar_C)/Delta P_C)). x = [P_C, Q_L].

	NOTES ERRATUM: the section says the elemental equations "are listed in
	the table, below", but the conversion kept only the cont/comp table; the
	elemental table (dP_C/dt = Q_C/C, dQ_L/dt = P_L/L, P_R = Q_R R(P_C)) is
	in the original, systems/ch_sim.tex.'''
	C, L, Rinf, R0, Pbar, dP = sympy.symbols('C L Rinf R0 Pbar dP')
	PC, QL, Qs = sympy.symbols('PC QL Qs')
	Rfun = '(Rinf + (R0 - Rinf)/2*(1 - tanh(5*(PC - Pbar)/dP)))'
	sys = solve(
		['Qs'],
		["PC' = QC/C", "QL' = PL/L"],
		['PR = QR*' + Rfun],
		['QC = Qs - QL', 'PL = PC - PR', 'QR = QL'],
		['PC', 'QL'])
	R = Rinf + (R0 - Rinf)/2*(1 - sympy.tanh(5*(PC - Pbar)/dP))
	assert_matrix('StateEq', sys.StateEq,
		[[(Qs - QL)/C], [(PC - QL*R)/L]])


def test_14_problems_sigmund():
	'''Ch. 14 nonlinear-systems-and-linearization/problems.md#sigmund: series V_s,
	R, L and a nonlinear capacitor q_C = k v_C^(3/2), so dv_C/dt =
	2 i_C/(3 k sqrt(v_C)). Checks f(x, u) and the linearization at
	x_o = [5, 0], u_o = [5].'''
	k, L, R = sympy.symbols('k L R')
	vC, iL, Vs = sympy.symbols('vC iL Vs')
	sys = solve(
		['Vs'],
		["vC' = 2/(3*k*sqrt(vC))*iC", "iL' = vL/L"],
		['vR = iR*R'],
		['iC = iL', 'vL = -vR + Vs - vC', 'iR = iL'],
		['vC', 'iL'])
	assert_matrix('StateEq', sys.StateEq,
		[[2/(3*k*sympy.sqrt(vC))*iL], [(-R*iL + Vs - vC)/L]])
	op = {vC: 5, iL: 0, Vs: 5}
	assert_matrix('A(x_o)', _plain(sys.A).subs(op),
		[[0, 2/(3*k*sympy.sqrt(5))], [-1/L, -R/L]])
	assert_matrix('B(x_o)', _plain(sys.B).subs(op), [[0], [1/L]])


def test_14_problems_franz():
	'''Ch. 14 nonlinear-systems-and-linearization/problems.md#franz: series V_s, C,
	L, R and a diode i_D = I_s (exp(v_D/V_TH) - 1). Checks f(x, u) and the
	linearization at x_o = [0, 0], u_o = [0]. The saturation current I_s is
	Isat here.

	The diode is a branch (i_D = i_L), so its equation solved for the
	primary variable is v_D = V_TH ln(i_D/I_s + 1), as the solution itself
	finds before substituting; the table's i_D = I_s(...) form is not.'''
	C, L, R, Isat, VTH = sympy.symbols('C L R Isat VTH')
	vC, iL, Vs = sympy.symbols('vC iL Vs')
	sys = solve(
		['Vs'],
		["vC' = iC/C", "iL' = vL/L"],
		['vR = iR*R', 'vD = VTH*log(iD/Isat + 1)'],
		['iC = iL', 'vL = -vD - vR + Vs - vC', 'iR = iL', 'iD = iL'],
		['vC', 'iL'])
	assert_matrix('StateEq', sys.StateEq,
		[[iL/C], [(-VTH*sympy.log(iL/Isat + 1) - R*iL + Vs - vC)/L]])
	op = {vC: 0, iL: 0, Vs: 0}
	assert_matrix('A(x_o)', _plain(sys.A).subs(op),
		[[0, 1/C], [-1/L, -(VTH/Isat + R)/L]])
	assert_matrix('B(x_o)', _plain(sys.B).subs(op), [[0], [1/L]])
