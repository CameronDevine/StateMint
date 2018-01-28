from sympy import *
import StateModelRnD
import sys

InVars = []
StVarElEqns = []
OtherElEqns = []
Constraints = []
OutputVars  = []

Atest = []
Btest = []
Ctest = []
Dtest = []
Etest = []
Ftest = []

# Test Systems

# Systems that I can't figure out how to make work,
skip = [2, 14, 15]

# System 1
# Garbini's Test Suite Quarter Car Model
InVars.append("vS")
StVarElEqns.append("vMB' = 1/MB * fMB, vMW' = 1/MW * fMW, fKS' = KS * vKS, fKT' = KT * vKT")
OtherElEqns.append("fBS = BS * vBS, fBT = BT * vBT")
Constraints.append("fMB = fKS + fBS, fMW = fKT + fBT - fKS - fBS, vKS = vMW - vMB, vKT = vS - vMW, vBS = vMW - vMB, vBT = vS - vMW")
OutputVars.append("vMB, vMW, fKS, fKT, fBS, fBT")

Atest.append('Matrix([[-BS/MB,BS/MB,1/MB,0],[BS/MW,(-BS-BT)/MW,-1/MW,1/MW],[-KS,KS,0,0],[0,-KT,0,0]])')
Btest.append('Matrix([[0],[BT/MW],[0],[KT]])')
Ctest.append('Matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[-BS,BS,0,0],[0,-BT,0,0]])')
Dtest.append('Matrix([[0],[0],[0],[0],[0],[BT]])')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 2
# Garbini's Test Suite DC Motor/Pulley
InVars.append("vI")
StVarElEqns.append("oJM'=1/JM*tJM")
OtherElEqns.append("iR=1/R*vR,v1=-Km*o2,t2=Km*i1,tB=B*oB,t3=-1/n*t4,o4=1/n*o3,tJL=JL*oJL'")
Constraints.append("tJM=-t2-tB-t3,vR=vI-v1,o2=oJM,i1=iR,oB=oJM,t4=-tJL,o3=oJM,oJL=o4")
OutputVars.append("oJM, oJL, iR, vR")

#Atest.append('Matrix([[(-B*n**2)/(JL+JM*n**2)]])')
Atest.append('Matrix([[-B/JM]])')
Btest.append('Matrix([[0]])')
Ctest.append('Matrix([[1],[1/n],[Km/R],[Km]])')
Dtest.append('Matrix([[0],[0],[1/R],[1]])')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 3
# Garbini's Test Suite Inertial Actuator
InVars.append("ec, vs")
StVarElEqns.append("vM'=1/M*fM,fK'=K*vK")
OtherElEqns.append("fB=B*vB,iR=1/R*vR,e1=-Km*V2,f2=Km*i1")
Constraints.append("fM=-f2-fB-fK,vK=vM-vs,vB=vM-vs,vR=ec-e1,V2=vM-vs,i1=iR")
OutputVars.append("fM")

Atest.append('Matrix([[-(Km**2+B*R)/(M*R),-1/M],[K,0]])')
Btest.append('Matrix([[-Km/(M*R),-(-Km**2-B*R)/(M*R)],[0,-K]])')
Ctest.append('Matrix([[-(Km**2+B*R)/R,-1]])')
Dtest.append('Matrix([[-Km/R,-(-Km**2-B*R)/R]])')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 4
# Garbini's Test Suite ME 471 Problem
InVars.append("vs")
StVarElEqns.append("oJ'=1/J*tJ,tK'=K*oK")
OtherElEqns.append("iR=1/R*vR,v1=Km*o2,t2=-Km*i1")
Constraints.append("tJ=-t2-tK,oK=oJ,vR=vs-v1,o2=oJ,i1=iR")
OutputVars.append("tK, oJ")

Atest.append('Matrix([[-Km**2/(J*R),-1/J],[K,0]])')
Btest.append('Matrix([[Km/(J*R)],[0]])')
Ctest.append('Matrix([[0,1],[1,0]])')
Dtest.append('Matrix([[0],[0]])')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 5
# Rowell and Wormley Example 5.1
InVars.append("Vs")
StVarElEqns.append("vC'=iC / C, iL'=vL / L")
OtherElEqns.append("iR=vR / R")
Constraints.append("iC = iR - iL, vL=vC, vR = Vs - vC")
OutputVars.append("iR, vR, vL, iC")

Atest.append('Matrix([[-1/(R*C), -1/C], [1/L, 0]])')
Btest.append('Matrix([[1/(R*C)],[0]])')
Ctest.append('Matrix([[-1/R,0],[-1,0],[1,0],[-1/R,-1]])')
Dtest.append('Matrix([[1/R],[1],[0],[1/R]])')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 6
# Rowell and Wormley Example 5.2
InVars.append("Fs")
StVarElEqns.append("vm' = Fm / m, Fk' = K * vk")
OtherElEqns.append("")
Constraints.append("Fm = Fs - Fk, vk = vm")
OutputVars.append("vm")

Atest.append('Matrix([[0,-1/m],[K,0]])')
Btest.append('Matrix([[1/m],[0]])')
Ctest.append('Matrix([[1,0]])')
Dtest.append('Matrix([[0]])')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 7
# Rowell and Wormley Example 5.3
InVars.append('Fs')
StVarElEqns.append("vm' = Fm / m, Fk' = K * vk")
OtherElEqns.append('FB = B * vB')
Constraints.append('Fm = Fs - FB - Fk,vk = vm,vB=vm')
OutputVars.append('vm, Fk')

Atest.append('Matrix([[-B/m,-1/m],[K,0]])')
Btest.append('Matrix([[1/m],[0]])')
Ctest.append('eye(2)')
Dtest.append('zeros(2,1)')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 8
# Rowell and Wormley Example 5.4
# In Equation (iii) 1 and 2 need to be switched
InVars.append("ws")
StVarElEqns.append("wj' = Tj / J")
OtherElEqns.append("TB1 = B1 * wB1, TB2 = B2 * wB2")
Constraints.append("Tj = TB2 - TB1, wB2 = ws - wj, wB1 = wj")
OutputVars.append("wj")

Atest.append('Matrix([[-(B1 + B2)/J]])')
Btest.append('Matrix([[B2/J]])')
Ctest.append('Matrix([[1]])')
Dtest.append('Matrix([[0]])')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 9
# Rowell and Wormley Example 5.5
InVars.append("Vs")
StVarElEqns.append("vC' = iC / C, iL' = vL / L")
OtherElEqns.append("vR = R * iR")
Constraints.append("iC = iL, iR = iL, vL = Vs - vR - vC")
OutputVars.append("vL, iC, vC")

Atest.append('Matrix([[0,1/C],[-1/L,-R/L]])')
Btest.append('Matrix([[0],[1/L]])')
Ctest.append('Matrix([[-1,-R],[0,1],[1,0]])')
Dtest.append('Matrix([[1],[0],[0]])')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 10
# Rowell and Wormley Example 5.6
InVars.append("Ps")
StVarElEqns.append("PC' = QC/C, QIp' = PIp/Ip")
OtherElEqns.append("PRp = Rp * QRp, QR1 = PR1/R1")
Constraints.append("QC = QIp - QR1, QRp = QIp, PIp = Ps - PRp - PC, PR1 = PC")
OutputVars.append("PC, QIp")

Atest.append('Matrix([[-1/(R1 * C),1/C],[-1/Ip,-Rp/Ip]])')
Btest.append('Matrix([[0],[1/Ip]])')
Ctest.append('eye(2)')
Dtest.append('zeros(2,1)')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 11
# Rowell and Wormley Example 5.7
InVars.append("Qs")
StVarElEqns.append("Tc' = qC / C")
OtherElEqns.append("TR2 = R2 * qR2, qR1 = TR1 / R1")
Constraints.append("qC = qR1, qR2 = Qs - qR1, TR1 = TR2 - Tc")
OutputVars.append("Tc")

Atest.append('Matrix([[-1/(C*(R1+R2))]])')
Btest.append('Matrix([[R2/(C*(R1+R2))]])')
Ctest.append('Matrix([[1]])')
Dtest.append('Matrix([[0]])')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 12
# Rowell and Wormley Example 5.9
InVars.append("Fs")
StVarElEqns.append("vm' = Fm/m, FK1' = K1 * vK1")
OtherElEqns.append("FB2 = B2 * vB2, vB1 = FB1/B1, vK2 = FK2' / K2")
Constraints.append("vK1 = vK2 - vB1, vB2 = vm, FK2 = Fs - FK1, FB1 = FK1, Fm = Fs - FB2")
OutputVars.append("vB1")

Atest.append('Matrix([[-B2/m,0],[0,-(K1 * K2)/(B1 * (K1 + K2))]])')
Btest.append('Matrix([[1/m],[0]])')
Ctest.append('Matrix([[0, 1/B1]])')
Dtest.append('Matrix([[0]])')
Etest.append('Matrix([[0],[K1/(K1+K2)]])')
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 13
# Rowell and Wormley Example 5.11
InVars.append("Fp, F0")
StVarElEqns.append("vm' = Fm / m")
OtherElEqns.append("Fd = cd * vd**2")
Constraints.append("Fm = Fp - F0 - Fd, vd = vm")
OutputVars.append("vm")

Atest.append('Matrix([[-2 * cd * vm(t) / m]])')
Btest.append('Matrix([[1/m,-1/m]])')
Ctest.append('Matrix([[1]])')
Dtest.append('Matrix([[0,0]])')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 14
# Rowell and Wormley Example 5.12
InVars.append("Ts")
StVarElEqns.append("wj' = Tj / J, TK' = m*g*l*cos(theta)*wK")
OtherElEqns.append("TB = B * wB")
Constraints.append("TK = -Tj - TB + Ts, wB = wj, wK = wj")
OutputVars.append("TK")

Atest.append('Matrix([[-B / J, -1 / J],[m*g*l*cos(theta), 0]])')
Btest.append('Matrix([[1/J],[0]])')
Ctest.append('Matrix([[0],[1]])')
Dtest.append('Matrix([[0]])')
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))

# System 15
# Rowell and Wormley Example 5.13
InVars.append("Qs")
StVarElEqns.append("QI' = PI / i, PC' = QC / (KT0 + (KT1 * PC) + (KT2 * PC**2))")
OtherElEqns.append("QR1 = K1 * sqrt(abs(PR1)) * sign(PR1), PR2 = QR2 * abs(QR2) / (K2**2)")
Constraints.append("QC = Qs - QR1, QR2 = QI, PR1 = PC, PI = PC - PR2")
OutputVars.append("QI, PC")

Atest.append('Matrix([[-(QI(t)*Derivative(abs(QI(t)), QI(t)) + abs(QI(t)))/(K2**2*i), 1/i], [0, (-K1*(2*abs(PC(t))*Derivative(sign(PC(t)), PC(t)) + sign(PC(t))*Derivative(abs(PC(t)), PC(t)))*(KT0 + KT1*PC(t) + KT2*PC(t)**2)/2 + (KT1 + 2*KT2*PC(t))*(K1*sqrt(abs(PC(t)))*sign(PC(t)) - Qs(t))*sqrt(abs(PC(t))))/((KT0 + KT1*PC(t) + KT2*PC(t)**2)**2*sqrt(abs(PC(t))))]])')
Btest.append('Matrix([[0],[1 / (KT0 + (KT1 * PC(t)) + (KT2 * PC(t)**2))]])')
Ctest.append('eye(2)')
Dtest.append(str(zeros(*sympify(Btest[-1]).shape)))
Etest.append(str(zeros(*sympify(Btest[-1]).shape)))
Ftest.append(str(zeros(*sympify(Dtest[-1]).shape)))



# Parse Args

test = range(len(InVars))
if len(sys.argv) >= 2:
	test = [int(sys.argv[1]) - 1]

# Test

for i in test:
	print "System " + str(i+1) + ":",
	if i+1 in skip:
		print "Skipped"
	else:
		sys = StateModelRnD.find(InVars[i], StVarElEqns[i], OtherElEqns[i], Constraints[i], OutputVars[i])
		A = sys['A']
		B = sys['B']
		C = sys['C']
		D = sys['D']
		E = sys['E']
		F = sys['F']
		tests = [simplify(A - sympify(Atest[i])) == zeros(A.shape[0], A.shape[1]),
			simplify(B - sympify(Btest[i])) == zeros(B.shape[0], B.shape[1]),
			simplify(C - sympify(Ctest[i])) == zeros(C.shape[0], C.shape[1]),
			simplify(D - sympify(Dtest[i])) == zeros(D.shape[0], D.shape[1]),
			simplify(E - sympify(Etest[i])) == zeros(E.shape[0], E.shape[1]),
			simplify(F - sympify(Ftest[i])) == zeros(F.shape[0], F.shape[1])]
		if False not in tests:
			print "Passed"
		else:
			print "Failed"
			calculated = [A, B, C, D, E, F]
			test = [Atest[i], Btest[i], Ctest[i], Dtest[i], Etest[i], Ftest[i]]
			for j in range(len(tests)):
				if not tests[j]:
					print "Calculated", chr(65 + j)
					pprint(calculated[j])
					print "Test", chr(65 + j)
					pprint(sympify(test[j]))		
