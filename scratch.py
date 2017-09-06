import operator
import math
length = 4
N = 8

maxWord = 2**N
maxVal = 2**(N*length)

def arrToInt(arr):
	return sum(maxWord**idx * word for idx, word in enumerate(arr))

def intToArr(val):
	out = []
	while val:
		out.append(val % maxWord)
		val //= maxWord
	while len(out) < length:
		out.append(0)
	return out


def mul(x, y):
	global overflow
	ac = [0]*length*2
	carry = 0
	for idx, val in enumerate(x):
		for idx2, val2 in enumerate(y):
			partial = val * val2 + carry
			carry, partial = divmod(partial, maxWord)
			ac[idx + idx2] += partial
		ac[idx + idx2 + 1] += carry
		carry = 0
	# ac[-1] = carry
	return ac

def test(func, op):
	for i in range(100):
		X = hash(str(i)) % maxVal
		Y = hash(chr(i)) % maxVal
		x = intToArr(X)
		y = intToArr(Y)
		r = func(x,y)
		R = op(X,Y)
		rVal = intToFloat(arrToInt(r))
		# rVal = r
		if R != rVal:
			print(X, Y, R, rVal)
		assert R == rVal

def truncate(mulRes):
	start = length - 1
	stop = start + length
	return mulRes[start:stop]

def intToFloat(X):
	return X / 2**(length*N - N)

def floatToInt(Xf):
	return int(Xf * 2**(length*N - N))

def floatMulInt(X, Y):
	Xf = toFloat(X)
	Yf = toFloat(Y)
	return floatToInt(Xf*Yf)

def floatMulArr(x, y):
	z = mul(x, y)
	return intToFloat(arrToInt(truncate(z)))

# print(intToFloat(maxVal))

# test(floatMulArr, operator.mul)
for i in range(100):
	X = hash(str(i)) % maxVal // 256
	Y = hash(chr(i)) % maxVal // 256
	x = intToArr(X)
	y = intToArr(Y)
	r = truncate(mul(x,y))
	Rf = intToFloat(arrToInt(r))
	Xf = intToFloat(X)
	Yf = intToFloat(Y)
	if not math.isclose(Rf, Xf*Yf):
	# if Rf != Xf*Yf:
		print(Xf*Yf, Rf)
	# assert Rf == Xf*Yf
