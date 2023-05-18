import time
start = time.time()
import functools
import random
import math
import sys
sys.set_int_max_str_digits(10**7)

replies = {
	3: "Fizz",
	5: "Buzz",
	#7: "Pop",
}

@functools.lru_cache(maxsize=None)
def chk(minIncl, maxExcl):
	s = ""
	for i in range(minIncl, maxExcl):
		replied = False
		for k, v in replies.items():
			if i % k == 0:
				s += v
				replied = True
		if not replied:
			s += str(i)
		s += "\n"
	return s 

groupSize = functools.reduce(lambda a, b: math.lcm(a, b), replies.keys())

def lenOfGroup(d):
	# fast because it only goes up to groupSize
	return len(chk(10**(d - 1), 10**(d - 1) + groupSize))

@functools.lru_cache(maxsize=None)
def lenForDigits(d):
	# length of fizzbuzz for all numbers that are "d" decimal digits long

	first = 10**(d - 1)
	last = 10**d

	skipAtBegin = (groupSize - first % groupSize) % groupSize # can't happen in normal fizzbuzz because no power of 10 is divisible by 15, but can happen in custom fizzbuzzpop
	skipAtEnd = last % groupSize

	groups = ((last - skipAtEnd) - (first + skipAtBegin)) // groupSize

	if groups < 0:
		# group size is big, for example this happens with fizzbuzz (groupSize = 15) and d=1 (only ten numbers) and 10 is less than 15
		return len(chk(first, last))

	extraAtBegin = chk(first, first + skipAtBegin) # this is at most groupSize lines, so, fast to compute
	extraAtEnd = chk(last - skipAtEnd, last) # same here

	return len(extraAtBegin) + len(extraAtEnd) + groups * lenOfGroup(d)

def calcIdx(idx):
	d = 1
	while lenForDigits(d) <= idx:
		idx -= lenForDigits(d)
		d += 1

	# we want a character from the range of fizzbuzz where "d"-digit numbers are being printed

	first = 10**(d - 1)
	last = 10**d
	
	skipAtBegin = (groupSize - first % groupSize) % groupSize # can't happen in normal fizzbuzz because no power of 10 is divisible by 15, but can happen in custom fizzbuzzpop
	skipAtEnd = last % groupSize

	extraAtBegin = chk(first, first + skipAtBegin) # this is at most groupSize lines, so, fast to compute
	extraAtEnd = chk(last - skipAtEnd, last) # same here

	if idx < len(extraAtBegin):
		return extraAtBegin[idx]

	if idx >= lenForDigits(d) - len(extraAtEnd):
		return extraAtEnd[idx - (lenForDigits(d) - len(extraAtEnd))]

	lenOfEachGroup = lenOfGroup(d)
	whichGroup = (idx - len(extraAtBegin)) // lenOfEachGroup
	indexIntoGroup = (idx - len(extraAtBegin)) % lenOfEachGroup

	groupStart = first + skipAtBegin + whichGroup * groupSize
	return chk(groupStart, groupStart + groupSize)[indexIntoGroup]

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
		print("Character", "2^" + str(i), "of FizzBuzz is", c)
		verify += c
	#print(verify)
	end = time.time()
	print("bench routine took", end-start, "seconds", file=sys.stderr)

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
