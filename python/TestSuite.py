from sympy import *
import StateMint
import StateMint.to_numpy
import numpy as np
import unittest

class TestStateMint(unittest.TestCase):

	def assertMatrixEqual(self, name, test, true):
		if test is not Matrix:
			test = sympify(test)
		if true is not Matrix:
			true = sympify(true)
		self.assertEqual(
			simplify(test - true),
			zeros(*true.shape),
			'Bad {} matrix,\n{}\nNot equal to,\n{}'.format(
				name,
				pretty(test, use_unicode = False),
				pretty(true, use_unicode = False)))

	def assertEquationEqual(self, name, test, true):
		if test is not Matrix:
			test = sympify(test)
		if true is not Matrix:
			true = sympify(true)
		self.assertEqual(
			simplify(test - true),
			zeros(*true.shape),
			'Bad {} equation,\n{}\nNot equal to,\n{}'.format(
				name,
				pretty(test, use_unicode = False),
				pretty(true, use_unicode = False)))

	def testSystem1(self):
		'''Garbini's Test Suite Quarter Car Model'''

		InVars = [
			"vS"]
		StVarElEqns = [
			"vMB' = 1/MB * fMB",
			"vMW' = 1/MW * fMW",
			"fKS' = KS * vKS",
			"fKT' = KT * vKT"]
		OtherElEqns = [
			"fBS = BS * vBS",
			"fBT = BT * vBT"]
		Constraints = [
			"fMB = fKS + fBS",
			"fMW = fKT + fBT - fKS - fBS",
			"vKS = vMW - vMB",
			"vKT = vS - vMW",
			"vBS = vMW - vMB",
			"vBT = vS - vMW"]
		OutputVars = [
			"vMB",
			"vMW",
			"fKS",
			"fKT",
			"fBS",
			"fBT"]

		Atest = 'Matrix([[-BS/MB,BS/MB,1/MB,0],[BS/MW,(-BS-BT)/MW,-1/MW,1/MW],[-KS,KS,0,0],[0,-KT,0,0]])'
		Btest = 'Matrix([[0],[BT/MW],[0],[KT]])'
		Ctest = 'Matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[-BS,BS,0,0],[0,-BT,0,0]])'
		Dtest = 'Matrix([[0],[0],[0],[0],[0],[BT]])'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem2(self):
		'''Garbini's Test Suite DC Motor/Pulley'''
		InVars = [
			"vI"]
		StVarElEqns = [
			"oJM'=1/JM*tJM"]
		OtherElEqns = [
			"iR=1/R*vR",
			"v1=-Km*o2",
			"t2=Km*i1",
			"tB=B*oB",
			"t3=-1/n*t4",
			"o4=1/n*o3",
			"tJL=JL*oJL'"]
		Constraints = [
			"tJM=-t2-tB-t3",
			"vR=vI-v1",
			"o2=oJM",
			"i1=iR",
			"oB=oJM",
			"t4=-tJL",
			"o3=oJM",
			"oJL=o4"]
		OutputVars = [
			"oJM",
			"oJL",
			"iR",
			"vR"]

		Atest = 'Matrix([[-(n**2*Km**2+n**2*R*B)/(R*n**2*JM+JL*R)]])'
		Btest = 'Matrix([[(-n**2*Km)/(R*n**2*JM+R*JL)]])'
		Ctest = 'Matrix([[1],[1/n],[Km/R],[Km]])'
		Dtest = 'Matrix([[0],[0],[1/R],[1]])'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem3(self):
		'''Garbini's Test Suite Inertial Actuator'''
		InVars = [
			"ec",
			"vs"]
		StVarElEqns = [
			"vM'=1/M*fM",
			"fK'=K*vK"]
		OtherElEqns = [
			"fB=B*vB",
			"iR=1/R*vR",
			"e1=-Km*V2",
			"f2=Km*i1"]
		Constraints = [
			"fM=-f2-fB-fK",
			"vK=vM-vs",
			"vB=vM-vs",
			"vR=ec-e1",
			"V2=vM-vs",
			"i1=iR"]
		OutputVars = [
			"fM"]

		Atest = 'Matrix([[-(Km**2+B*R)/(M*R),-1/M],[K,0]])'
		Btest = 'Matrix([[-Km/(M*R),-(-Km**2-B*R)/(M*R)],[0,-K]])'
		Ctest = 'Matrix([[-(Km**2+B*R)/R,-1]])'
		Dtest = 'Matrix([[-Km/R,-(-Km**2-B*R)/R]])'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem4(self):
		'''Garbini's Test Suite ME 471 Problem'''
		InVars = [
			"vs"]
		StVarElEqns = [
			"oJ'=1/J*tJ",
			"tK'=K*oK"]
		OtherElEqns = [
			"iR=1/R*vR",
			"v1=Km*o2",
			"t2=-Km*i1"]
		Constraints = [
			"tJ=-t2-tK",
			"oK=oJ",
			"vR=vs-v1",
			"o2=oJ",
			"i1=iR"]
		OutputVars = [
			"tK",
			"oJ"]

		Atest = 'Matrix([[-Km**2/(J*R),-1/J],[K,0]])'
		Btest = 'Matrix([[Km/(J*R)],[0]])'
		Ctest = 'Matrix([[0,1],[1,0]])'
		Dtest = 'Matrix([[0],[0]])'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem5(self):
		'''Rowell and Wormley Example 5.1'''
		InVars = [
			"Vs"]
		StVarElEqns = [
			"vC'=iC / C",
			"iL'=vL / L"]
		OtherElEqns = [
			"iR=vR / R"]
		Constraints = [
			"iC = iR - iL",
			"vL=vC",
			"vR = Vs - vC"]
		OutputVars = [
			"iR",
			"vR",
			"vL",
			"iC"]

		Atest = 'Matrix([[-1/(R*C), -1/C], [1/L, 0]])'
		Btest = 'Matrix([[1/(R*C)],[0]])'
		Ctest = 'Matrix([[-1/R,0],[-1,0],[1,0],[-1/R,-1]])'
		Dtest = 'Matrix([[1/R],[1],[0],[1/R]])'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem6(self):
		'''Rowell and Wormley Example 5.2'''
		InVars = [
			"Fs"]
		StVarElEqns = [
			"vm' = Fm / m",
			"Fk' = K * vk"]
		OtherElEqns = []
		Constraints = [
			"Fm = Fs - Fk",
			"vk = vm"]
		OutputVars = [
			"vm"]

		Atest = 'Matrix([[0,-1/m],[K,0]])'
		Btest = 'Matrix([[1/m],[0]])'
		Ctest = 'Matrix([[1,0]])'
		Dtest = 'Matrix([[0]])'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem7(self):
		'''Rowell and Wormley Example 5.3'''
		InVars = [
			'Fs']
		StVarElEqns = [
			"vm' = Fm / m",
			"Fk' = K * vk"]
		OtherElEqns = [
			'FB = B * vB']
		Constraints = [
			'Fm = Fs - FB - Fk',
			'vk = vm',
			'vB=vm']
		OutputVars = [
			'vm',
			'Fk']

		Atest = 'Matrix([[-B/m,-1/m],[K,0]])'
		Btest = 'Matrix([[1/m],[0]])'
		Ctest = 'eye(2)'
		Dtest = 'zeros(2,1)'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem8(self):
		'''Rowell and Wormley Example 5.4'''
		# In Equation (iii) 1 and 2 need to be switched
		InVars = [
			"ws"]
		StVarElEqns = [
			"wj' = Tj / J"]
		OtherElEqns = [
			"TB1 = B1 * wB1",
			"TB2 = B2 * wB2"]
		Constraints = [
			"Tj = TB2 - TB1",
			"wB2 = ws - wj",
			"wB1 = wj"]
		OutputVars = [
			"wj"]

		Atest = 'Matrix([[-(B1 + B2)/J]])'
		Btest = 'Matrix([[B2/J]])'
		Ctest = 'Matrix([[1]])'
		Dtest = 'Matrix([[0]])'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem9(self):
		'''Rowell and Wormley Example 5.5'''
		InVars = [
			"Vs"]
		StVarElEqns = [
			"vC' = iC / C",
			"iL' = vL / L"]
		OtherElEqns = [
			"vR = R * iR"]
		Constraints = [
			"iC = iL",
			"iR = iL",
			"vL = Vs - vR - vC"]
		OutputVars = [
			"vL",
			"iC",
			"vC"]

		Atest = 'Matrix([[0,1/C],[-1/L,-R/L]])'
		Btest = 'Matrix([[0],[1/L]])'
		Ctest = 'Matrix([[-1,-R],[0,1],[1,0]])'
		Dtest = 'Matrix([[1],[0],[0]])'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem10(self):
		'''Rowell and Wormley Example 5.6'''
		InVars = [
			"Ps"]
		StVarElEqns = [
			"PC' = QC/C",
			"QIp' = PIp/Ip"]
		OtherElEqns = [
			"PRp = Rp * QRp",
			"QR1 = PR1/R1"]
		Constraints = [
			"QC = QIp - QR1",
			"QRp = QIp",
			"PIp = Ps - PRp - PC",
			"PR1 = PC"]
		OutputVars = [
			"PC",
			"QIp"]

		Atest = 'Matrix([[-1/(R1 * C),1/C],[-1/Ip,-Rp/Ip]])'
		Btest = 'Matrix([[0],[1/Ip]])'
		Ctest = 'eye(2)'
		Dtest = 'zeros(2,1)'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem11(self):
		'''Rowell and Wormley Example 5.7'''
		InVars = [
			"Qs"]
		StVarElEqns = [
			"Tc' = qC / C"]
		OtherElEqns = [
			"TR2 = R2 * qR2",
			"qR1 = TR1 / R1"]
		Constraints = [
			"qC = qR1",
			"qR2 = Qs - qR1",
			"TR1 = TR2 - Tc"]
		OutputVars = [
			"Tc"]

		Atest = 'Matrix([[-1/(C*(R1+R2))]])'
		Btest = 'Matrix([[R2/(C*(R1+R2))]])'
		Ctest = 'Matrix([[1]])'
		Dtest = 'Matrix([[0]])'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertEqual(simplify(sys.A - sympify(Atest)), zeros(*sys.A.shape), 'Bad A matrix,\n{}\nNot equal to,\n{}'.format(sys.A, Atest))
		self.assertEqual(simplify(sys.B - sympify(Btest)), zeros(*sys.B.shape), 'Bad B matrix,\n{}\nNot equal to,\n{}'.format(sys.B, Btest))
		self.assertEqual(simplify(sys.C - sympify(Ctest)), zeros(*sys.C.shape), 'Bad B matrix,\n{}\nNot equal to,\n{}'.format(sys.C, Ctest))
		self.assertEqual(simplify(sys.D - sympify(Dtest)), zeros(*sys.D.shape), 'Bad D matrix,\n{}\nNot equal to,\n{}'.format(sys.D, Dtest))
		self.assertEqual(simplify(sys.E - sympify(Etest)), zeros(*sys.E.shape), 'Bad E matrix,\n{}\nNot equal to,\n{}'.format(sys.E, Etest))
		self.assertEqual(simplify(sys.F - sympify(Ftest)), zeros(*sys.F.shape), 'Bad F matrix,\n{}\nNot equal to,\n{}'.format(sys.F, Etest))

	def testSystem12(self):
		'''Rowell and Wormley Example 5.9'''
		InVars = [
			"Fs"]
		StVarElEqns = [
			"vm' = Fm/m",
			"FK1' = K1 * vK1"]
		OtherElEqns = [
			"FB2 = B2 * vB2",
			"vB1 = FB1/B1",
			"vK2 = FK2' / K2"]
		Constraints = [
			"vK1 = vK2 - vB1",
			"vB2 = vm",
			"FK2 = Fs - FK1",
			"FB1 = FK1",
			"Fm = Fs - FB2"]
		OutputVars = [
			"vB1"]

		Atest = 'Matrix([[-B2/m,0],[0,-(K1 * K2)/(B1 * (K1 + K2))]])'
		Btest = 'Matrix([[1/m],[0]])'
		Ctest = 'Matrix([[0, 1/B1]])'
		Dtest = 'Matrix([[0]])'
		Etest = 'Matrix([[0],[K1/(K1+K2)]])'
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem13(self):
		'''Rowell and Wormley Example 5.11'''
		InVars = [
			"Fp",
			"F0"]
		StVarElEqns = [
			"vm' = Fm / m"]
		OtherElEqns = [
			"Fd = cd * vd**2"]
		Constraints = [
			"Fm = Fp - F0 - Fd",
			"vd = vm"]
		OutputVars = [
			"vm"]

		Atest = 'Matrix([[-2 * cd * vm(t) / m]])'
		Btest = 'Matrix([[1/m,-1/m]])'
		Ctest = 'Matrix([[1]])'
		Dtest = 'Matrix([[0,0]])'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	def testSystem14(self):
		'''Rowell and Wormley Example 5.12'''
		InVars = [
			"Ts"]
		StVarElEqns = [
			"wj' = Tj / J",
			"TK' = m*g*l*cos(theta)*wK"]
		OtherElEqns = [
			"TB = B * wB"]
		Constraints = [
			"Tj = -TK - TB + Ts",
			"wB = wj",
			"wK = wj"]
		OutputVars = [
			"TK"]

		Atest = 'Matrix([[-B / J, -1 / J],[m*g*l*cos(theta), 0]])'
		Btest = 'Matrix([[1/J],[0]])'
		Ctest = 'Matrix([[0, 1]])'
		Dtest = 'Matrix([[0]])'
		Etest = str(zeros(*sympify(Btest).shape))
		Ftest = str(zeros(*sympify(Dtest).shape))

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertMatrixEqual('A', sys.A, Atest)
		self.assertMatrixEqual('B', sys.B, Btest)
		self.assertMatrixEqual('C', sys.C, Ctest)
		self.assertMatrixEqual('D', sys.D, Dtest)
		self.assertMatrixEqual('E', sys.E, Etest)
		self.assertMatrixEqual('F', sys.F, Ftest)

	@unittest.expectedFailure
	def testSystem15(self):
		'''Rowell and Wormley Example 5.13'''
		InVars = [
			"Qs"]
		StVarElEqns = [
			"QI' = PI / i",
			"PC' = QC / (KT0 + (KT1 * PC) + (KT2 * PC**2))"]
		OtherElEqns = [
			"QR1 = K1 * sqrt(abs(PR1)) * sign(PR1)",
			"PR2 = QR2 * abs(QR2) / (K2**2)"]
		Constraints = [
			"QC = Qs - QR1",
			"QR2 = QI",
			"PR1 = PC",
			"PI = PC - PR2"]
		OutputVars = [
			"QI",
			"PC"]

		StateTest = 'Matrix([[(1/i)*(PC(t)-(1/K2**2)*QI(t)*abs(QI(t)))],[1/(KT0+KT1*PC(t)+KT2*PC(t)**2)*(Qs(t)-K1*sqrt(abs(PC(t)))*sign(PC(t)))]])'
		OutputTest = 'Matrix([[QI(t)],[PC(t)]])'

		sys = StateMint.Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars)

		self.assertEquationEqual('State', sys.StateEq, StateTest)
		self.assertEquationEqual('Output', sys.OutEq, OutputTest)

class TestToArray(unittest.TestCase):

	def testMatrix1(self):
		matrix = sympify('Matrix([[-BS/MB,BS/MB,1/MB,0],[BS/MW,(-BS-BT)/MW,-1/MW,1/MW],[-KS,KS,0,0],[0,-KT,0,0]])')
		values = {
			'BS': 10,
			'MB': 5,
			'MW': 2,
			'BT': 15,
			'KS': 30,
			'KT': 20}
		array = StateMint.to_numpy.array(matrix, values)
		test = np.array([
			[-2, 2, 0.2, 0],
			[5, -12.5, -0.5, 0.5],
			[-30, 30, 0, 0],
			[0, -20, 0, 0]])
		self.assertEqual(matrix.shape, array.shape)
		self.assertTrue(isinstance(array, np.ndarray))
		self.assertTrue(np.all(array == test), 'Array\n{}\nIs not the correct matrix:\n{}'.format(array, test))

	def testMatrix2(self):
		matrix = sympify('Matrix([[0],[BT/MW],[0],[KT]])')
		values = {
			'MW': 2,
			'BT': 15,
			'KT': 20}
		array = StateMint.to_numpy.array(matrix, values)
		test = np.array([
			[0],
			[7.5],
			[0],
			[20]])
		self.assertEqual(matrix.shape, array.shape)
		self.assertTrue(isinstance(array, np.ndarray))
		self.assertTrue(np.all(array == test), 'Array\n{}\nIs not the correct matrix:\n{}'.format(array, test))

if __name__ == '__main__':
	unittest.main()
