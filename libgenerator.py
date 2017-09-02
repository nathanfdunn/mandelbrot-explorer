import math
bits = 16
N = math.floor((bits - 1)/2)
N = 4

length = 2

carry = 0
overflow = False

maxWord = 2**N
maxVal = 2**(N*length) - 1
# mulMax = 3			

# These are ordered least significant to most
# Accumulator
ac = [0]*length

x = [0]*length

y = [0]*length

def add(x, y):
	global overflow
	overflow = False
	carry = 0
	ac = [0]*length
	for i in range(length):
		ac[i] = x[i] + y[i] + carry
		if ac[i] > maxWord:
			# We know that it can only ever
			# overflow by one unit
			# print('addition overflow', divmod(ac[i], maxWord))
			carry = 1
			ac[i] %= maxWord
		else:
			carry = 0
	if carry > 0:
		overflow = True
	return ac

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

def arrToVal(arr):
	return sum(maxWord**idx * word for idx, word in enumerate(arr))

def valToArr(val):
	out = []
	while val:
		out.append(val % maxWord)
		val //= maxWord
	while len(out) < length:
		out.append(0)
	return out

for i in range(100):
	val = hash(str(i)) % maxVal
	# print(str(val).ljust(20), str(valToArr(val)).ljust(20))
	assert val == arrToVal(valToArr(val))

for i in range(100):
	val1 = hash(str(i)) % (maxVal)
	val2 = hash(chr(i)) % (maxVal)
	arr1 = valToArr(val1)
	arr2 = valToArr(val2)
	arrr = add(arr1, arr2)
	valr = arrToVal(arrr)
	if not overflow:
		assert valr == val1 + val2
	else:
		assert valr == val1 + val2 - (maxVal + 1)

def trymul(a,b):
	res = mul(valToArr(a),valToArr(b))
	return res, arrToVal(res), a*b

# print(trymul(2,8))

for i in range(100):
	val1 = hash(str(i)) % maxVal
	val2 = hash(chr(i)) % maxVal
	arr1 = valToArr(val1)
	arr2 = valToArr(val2)
	arrr = mul(arr1, arr2)
	valr = arrToVal(arrr)
	try:
		assert valr == val1 * val2
	except:
		print(arr1, arr2, arrr)
