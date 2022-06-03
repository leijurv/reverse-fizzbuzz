import functools
import random

@functools.lru_cache(maxsize=None)
def chk(minIncl, maxExcl):
	s = ""
	for i in range(minIncl, maxExcl):
		if i % 15 == 0:
			s += "FizzBuzz"
		elif i % 3 == 0:
			s += "Fizz"
		elif i % 5 == 0:
			s += "Buzz"
		else:
			s += str(i)
		s += "\n"
	return s 

@functools.lru_cache(maxsize=None)
def lenOfGroupOf15(digits):
	# fast because it only goes up to 15
	s = 0
	for i in range(15):
		if i % 15 == 0:
			s += len("FizzBuzz")
		elif i % 3 == 0:
			s += len("Fizz")
		elif i % 5 == 0:
			s += len("Buzz")
		else:
			s += digits
		s += len("\n")
	return s

@functools.lru_cache(maxsize=None)
def lenForDigits(d):
	# length of fizzbuzz for all numbers that are "d" decimal digits long

	if d == 1:
		# there are less than 15 numbers 1 through 10, so the math of splitting into 15-groups doesn't work
		return len(chk(1, 10)) # this is just 30, so no big deal
	first = 10**(d - 1)
	last = 10**d
	
	skipAtBegin = 15 - first % 15 # no power of 10 is divisible by 15
	skipAtEnd = last % 15

	extraAtBegin = chk(first, first + skipAtBegin) # this is at most 15 lines, so, fast to compute
	extraAtEnd = chk(last - skipAtEnd, last) # same here

	groupsOf15 = ((last - skipAtEnd) - (first + skipAtBegin)) // 15
	return len(extraAtBegin) + len(extraAtEnd) + groupsOf15 * lenOfGroupOf15(d)

def calcIdx(idx):
	d = 1
	while lenForDigits(d) <= idx:
		idx -= lenForDigits(d)
		d += 1

	# we want a character from the range of fizzbuzz where "d"-digit numbers are being printed

	first = 10**(d - 1)
	last = 10**d
	
	skipAtBegin = 15 - first % 15 # no power of 10 is divisible by 15
	skipAtEnd = last % 15

	extraAtBegin = chk(first, first + skipAtBegin) # this is at most 15 lines, so, fast to compute
	extraAtEnd = chk(last - skipAtEnd, last) # same here

	if idx < len(extraAtBegin):
		return extraAtBegin[idx]
	if idx >= lenForDigits(d) - len(extraAtEnd):
		return extraAtEnd[idx - (lenForDigits(d) - len(extraAtEnd))]

	lenOfEachGroup = lenOfGroupOf15(d)
	whichGroupOfFifteen = (idx - len(extraAtBegin)) // lenOfEachGroup
	indexIntoGroupOfFifteen = (idx - len(extraAtBegin)) % lenOfEachGroup
	fifteenGroupStart = first + skipAtBegin + whichGroupOfFifteen * 15
	return chk(fifteenGroupStart, fifteenGroupStart + 15)[indexIntoGroupOfFifteen]

if False:
	print(chk(1, 20))

if True: # verification routine
	random.seed(137)
	maxN = 1234567
	chkStr = chk(1, maxN)
	for i in range(10000):
		if chkStr[i] != calcIdx(i):
			raise Exception("wrong " + str(i))
	for trial in range(10000):
		i = random.randint(0, len(chkStr) - 1)
		if chkStr[i] != calcIdx(i):
			raise Exception("wrong " + str(i))
	print("Verified")

if False:
	random.seed(137)
	verify = ""
	for i in range(2000):
		idx = random.randint(0, 10**i)
		c = calcIdx(idx)
		#print("Character", idx, "of FizzBuzz is", c)
		verify += c
	print(verify)

if True: # benchmark routine
	verify = ""
	for i in range(20000):
		#print(i)
		c = calcIdx(2**i)
		print("Character", 2**i, "of FizzBuzz is", c)
		verify += c
	#print(verify)

if False:
	random.seed(137)
	for trials in range(1000):
		idx = random.randint(0, 10**10000)
		c = calcIdx(idx)
		#print("Character", idx, "of FizzBuzz is", c)

if False:
	bench = ([lenForDigits(i) for i in range(1, 5000)])
	#print(len(bench))
	#print(bench)
