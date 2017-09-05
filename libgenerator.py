import random
import math
bits = 16
N = math.floor((bits - 1)/2)

length = 4

N = 4
length = 2

carry = 0
overflow = False

# Well...this is just wrong
maxWord = 2**N
maxVal = 2**(N*length) - 1

maxFloat = maxWord - 1
# mulMax = 3			

# These are ordered least significant to most
# Accumulator
ac = [0]*length

x = [0]*length

y = [0]*length

class Num:
	def __init__(self, arr, pos=True):
		self.arr = arr
		self.pos = pos
	def __neg__(self):
		return Num(self.arr, not self.pos)
	def __pos__(self):
		return self
	def __int__(self):
		return arrToVal(self.arr) if self.pos else -arrToVal(self.arr)
	def __repr__(self):
		return '-+'[self.pos] + f'Num({self.arr})'


	@classmethod
	def fromint(cls, val):
		if val >= 0:
			return Num(valToArr(val), True)
		else:
			return Num(valToArr(-val), False)

def cmp(arr1, arr2):
	for i in reversed(range(length)):
		if arr1[i] > arr2[i]:
			return 1
		elif arr2[i] > arr1[i]:
			return -1
	return 0

# Only for positive nums
def addNum(a: Num, b: Num) -> Num:
	assert a.pos and b.pos
	return Num(add(a.arr, b.arr), True)

def subNum(a: Num, b: Num) -> Num:
	if a.pos and b.pos:
		if cmp(a.arr, b.arr) == -1:
			return -subNum(b, a)
		else:
			return Num(sub(a.arr, b.arr), True)
	elif a.pos and not b.pos:
		return addNum(a, -b)
	elif not a.pos and not b.pos:
		return -subNum(-a,-b)
	else: #  a < 0 and b > 0
		return -addNum(-a, b)


# WLOG assume a >= b
def sub(a: list, b: list) -> list:
	out = [0]*length
	# a[i+1] should never be out of bounds because of our
	# assumption a >= b
	for i in range(length):
		if a[i] < 0:
			# Borrow
			a[i] += maxWord
			a[i+1] -= 1

		temp = a[i] - b[i]
		if temp < 0:
			# Borrow
			temp += maxWord
			a[i+1] -= 1

		out[i] = temp
	return out

def add(x, y):
	global overflow
	overflow = False
	carry = 0
	ac = [0]*length
	for i in range(length):
		ac[i] = x[i] + y[i] + carry
		if ac[i] >= maxWord:
			# We know that it can only ever
			# overflow by one unit
			# print('addition overflow', divmod(ac[i], maxWord))
			carry = 1
			ac[i] -= maxWord
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

def mulNum(x: Num, y: Num):
	val = mul(x.arr, y.arr)
	return Num(val, x.pos == y.pos)

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

def tryadd(a,b):
	res = add(valToArr(a),valToArr(b))
	return res, arrToVal(res), a+b

def trymul(a,b):
	res = mul(valToArr(a),valToArr(b))
	return res, arrToVal(res), a*b

def trysub(a,b):
	res = sub(valToArr(a), valToArr(b))
	return res, arrToVal(res), a-b

def trysub2(a,b):
	expected = a - b
	a = Num.fromint(a)
	b = Num.fromint(b)
	res = subNum(a,b)
	return res, int(res), expected

# x -> x / 2**(length*N-k), where 2**k = maxFloat
# Since we want an easy conversion, we'll just
# round k up to N
# Ergo, we take the length-1 most significant words
# Note: this will influence cmp(int, float)
k = N
# Well, it is idempotent. But wrong
# And remember, the identity element in THIS
# group is not Num.fromint(1)
# It should be 2**(length*N-k)
# This should do the same thing(ish) as toFloat
# Wait...I don't think that's right
# So this is like dividing by by 2**(N+1)
def truncate(n: Num):
	# Ok, we're using our knowledge that maxFloat == maxWord now
	length*N - k
	# newarr = n.arr[-length:-1] + [0]
	# newarr = n.arr[-length-1:-1] + [0]	
	start = length - 1
	stop = start + length
	newarr = n.arr[start:stop]

	return Num(newarr, n.pos)

# # Oh look at that, x can be a regular int too
# def toFloat(x: Num) -> float:
# 	# return int(x) / 2**(length*N - k)
# 	# return int(x) * maxFloat / maxVal
# 	return int(x) / 2**(length*N - N)

# def fromFloat(x: float) -> Num:
# 	X = round(x * maxVal / maxFloat)
# 	# So this is trickier...I guess just round
# 	return Num.fromint(X)
# 	# res = int(x*2**(length*N - k))
# 	# return Num.fromint(res)

# def toFloatUntrunc(x: int):
# 	return int(x) / 2**(length*N+k)



# print(trymul(2,8))

# def verify(a,b,op):

for i in range(100):
	val1 = hash(str(i)) % maxVal
	val2 = hash(chr(i)) % maxVal
	arr1 = valToArr(val1)
	arr2 = valToArr(val2)
	arrr = mul(arr1, arr2)
	valr = arrToVal(arrr)
	assert valr == val1 * val2

trysub(2,1)

random.seed(1)
for i in range(100):
	val1 = random.randint(0, maxVal)
	val2 = random.randint(0, maxVal)
	# val1 = hash(str(i)) % maxVal
	# val2 = hash(chr(i)) % maxVal
	a, b = max(val1, val2), min(val1, val2)
	arr1 = valToArr(a)
	arr2 = valToArr(b)
	arrr = sub(arr1, arr2)
	valr = arrToVal(arrr)
	try:
		assert a-b == valr
		# print(a, b, valr, arr1, arr2, arrr)
	except:
		print(a, b, valr, arr1, arr2, arrr)

register = []
random.seed(382)
for i in range(100):
	# dividing by 2 so we don't have overflow
	val1 = random.randint(-maxVal//2, maxVal//2)
	val2 = random.randint(-maxVal//2, maxVal//2)
	n1 = Num.fromint(val1)
	n2 = Num.fromint(val2)
	res = subNum(n1, n2)
	if val1 - val2 != int(res):
		register.append(i)
		print(val1, val2, int(res), n1, n2, res, val1-val2)

# for i in range(100):
# 	val = hash(str(i)) % maxVal
# 	assert val == int(fromFloat(toFloat(val))), 'no good ' + str(val)

# for i in range(100):
# 	X = random.randint(-maxVal, maxVal)
# 	Y = random.randint(-maxVal, maxVal)
# 	x = toFloat(X)
# 	y = toFloat(Y)
# 	expected = x*y
# 	actual = toFloat(X*Y)
# 	assert math.isclose(expected, actual), f'Nope: {X}, {Y}, {X*Y}, {x}, {y}, {expected}, {actual}'



# for i in range(100):
# 	# Ok, I figured out what was going on
# 	# (I think). It wasn't matching up
# 	# because we rely on not leaving
# 	# the plausible range of floats...
# 	val1 = random.randint(-maxVal, maxVal)
# 	val2 = random.randint(-maxVal, maxVal)
# 	# val1 = random.randint(-maxWord, maxWord)
# 	# val2 = random.randint(-maxWord, maxWord)
# 	x1 = Num.fromint(val1)
# 	x2 = Num.fromint(val2)
# 	numRes = mulNum(x1, x2)
# 	truncNum = truncate(numRes)
# 	res = toFloat(truncNum)
# 	y1 = toFloat(x1)
# 	y2 = toFloat(x2)
# 	assert math.isclose(res, y1*y2), f'Nope: {val1}, {val2}, {y1}, {y2}, {y1*y2}, {res}'
# 	print(val1, val2, y1, y2, y1*y2, res)

