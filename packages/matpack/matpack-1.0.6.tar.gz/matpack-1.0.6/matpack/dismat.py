from numpy import zeros, math
from sympy import Symbol, symarray, expand
def progressive1d(array,choice):
	order= len(array)-1
	value = zeros((order + 1, order + 2))
	for i in range(0, order + 1):
		value[0][i] = array[i]
	for i in range(0, order):
		for j in range(0, order):
			if choice == "arithmetic":
				value[i + 1][j] = value[i][j + 1] - value[i][j]
			elif choice == "geometric":
				value[i + 1][j] = value[i][j + 1] / value[i][j]
	x = Symbol("x")
	if choice=="arithmetic":
		g = 1
		f = 0
		for i in range(1, order + 1):
			g = g * (x - i)
			f = f + (g * value[i][0]) / math.factorial(i)
		f = f + value[0][0]
	if choice=="geometric":
		g = 1
		f = 1
		for i in range(1, order + 1):
			g = g * (x - i)
			f = f * (value[i][0] ** (g / math.factorial(i)))
		f = f * value[0][0]
	h = expand(f)
	return h

def progressive2d(matrix, choice):
	order = len(matrix) - 1
	matrizdascolunas = zeros((order + 1, order + 1))
	f = symarray('x', (1, order + 1))
	x = Symbol("x")
	if choice=="arithmetic":
		for k in range(0, order + 1):
			for i in range(0, order + 1):
				matrizdascolunas[0][i] = matrix[i][k]
			for i in range(0, order):
				for j in range(0, order - i):
					matrizdascolunas[i + 1][j] = matrizdascolunas[i][j + 1] - matrizdascolunas[i][j]
			g = 1
			f[0][k] = 0
			for i in range(1, order + 1):
				g = g * (x - i)
				f[0][k] = f[0][k] + (g * matrizdascolunas[i][0]) / math.factorial(i)
			f[0][k] = f[0][k] + matrizdascolunas[0][0]
			f[0][k] = expand(f[0][k])
		matrizfuncao = symarray('f', (order + 1, order + 1))
		for i in range(0, order + 1):
			matrizfuncao[0][i] = f[0][i]
		for i in range(0, order):
			for j in range(0, order - i):
				matrizfuncao[i + 1][j] = matrizfuncao[i][j + 1] - matrizfuncao[i][j]
		y = Symbol("y")
		g = 1
		f1 = 0
		for i in range(1, order + 1):
			g = g * (y - i)
			f1 = f1 + (g * matrizfuncao[i][0]) / math.factorial(i)
		f1 = f1 + matrizfuncao[0][0]
		h = expand(f1)
		return h
	if choice=="geometric":
		for k in range(0, order + 1):
			for i in range(0, order + 1):
				matrizdascolunas[0][i] = matrix[i][k]
			for i in range(0, order):
				for j in range(0, order - i):
					matrizdascolunas[i + 1][j] = matrizdascolunas[i][j + 1] / matrizdascolunas[i][j]
			g = 1
			f[0][k] = 1
			for i in range(1, order + 1):
				g = g * (x - i)
				f[0][k] = f[0][k] * matrizdascolunas[i][0]**(g / math.factorial(i))
			f[0][k] = f[0][k] * matrizdascolunas[0][0]
		matrizfuncao = symarray('f', (order + 1, order + 1))
		for i in range(0, order + 1):
			matrizfuncao[0][i] = f[0][i]
		for i in range(0, order):
			for j in range(0, order - i):
				matrizfuncao[i + 1][j] = matrizfuncao[i][j + 1] / matrizfuncao[i][j]
		y = Symbol("y")
		g = 1
		f1 = 1
		for i in range(1, order + 1):
			g = g * (y - i)
			f1 = f1 * matrizfuncao[i][0]**(g / math.factorial(i))
		f1 = f1 * matrizfuncao[0][0]
		return f1

