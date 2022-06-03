import functools
import random
import math

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

def precomputeData():
	charsFor = [""] * groupSize
	for i in range(groupSize):
		for k, v in replies.items():
			if i % k == 0:
				charsFor[i] += v
	charsUpToIncl = []
	runningTot = 0
	numsUpToIncl = []
	numsTot = 0
	for i in range(groupSize):
		runningTot += len(charsFor[i]) + 1
		numsTot += charsFor[i] == ""
		charsUpToIncl.append(runningTot)
		numsUpToIncl.append(numsTot)
	return charsFor, charsUpToIncl, numsUpToIncl

charsFor, charsUpToIncl, numsUpToIncl = precomputeData()

def lenFrom(maxExcl, digitLen): # length of fizzbuzz up to maxExcl when digits are digitLen long
	if maxExcl <= 0:
		if maxExcl == 0:
			return 0
		raise Exception("negative")
	return charsUpToIncl[maxExcl - 1] + numsUpToIncl[maxExcl - 1] * digitLen

@functools.lru_cache(maxsize=None)
def precomputedDataForDigits(d):
	if d <= 0:
		raise Exception("negative")
	if d < 10 or precomputedDataForDigits(d - 1)[2] < 0: # or if previous number of digits had a negative groupQuotient, in which case we can't use it without a bit of a headache
		# this is the base case, the computation that we are caching
		first = 10**(d - 1)
		last = 10**d
		skipAtBegin = (groupSize - first % groupSize) % groupSize
		skipAtEnd = last % groupSize

		groupDividend = ((last - skipAtEnd) - (first + skipAtBegin)) # last - first - (skipAtEnd + skipAtBegin)
		groupQuotient, groupRemainder = divmod(groupDividend, groupSize)
		return (skipAtBegin, skipAtEnd, groupQuotient, groupRemainder, first)

	prevSkipAtBegin, prevSkipAtEnd, quot, rem, prevFirst = precomputedDataForDigits(d - 1)
	skipAtBegin = (groupSize - prevSkipAtEnd) % groupSize
	skipAtEnd = (prevSkipAtEnd * 10) % groupSize

	rem += prevSkipAtBegin + prevSkipAtEnd # add back skipAtBegin and skipAtEnd that were previously subtracted out
	quot *= 10 # one more digit means quotient is ten times greater
	rem *= 10 # same for remainder
	rem += groupSize * 2 # make sure rem is big enough to subtract from
	quot -= 2 # balance out addition to rem
	rem -= skipAtBegin + skipAtEnd # this won't make rem negative due to the previous two lines
	quot += rem // groupSize # prevent rem from blowing up
	rem %= groupSize # balance out previous line's addition to quot
	return (skipAtBegin, skipAtEnd, quot, rem, prevFirst * 10)

@functools.lru_cache(maxsize=None)
def lenForDigits(d):
	# length of fizzbuzz for all numbers that are "d" decimal digits long
	skipAtBegin, skipAtEnd, groups, ignored, ignored2 = precomputedDataForDigits(d)

	if groups < 0:
		#print("Falling back for digit count", d)
		# group size is big, for example this happens with fizzbuzz (groupSize = 15) and d=1 (only ten numbers) and 10 is less than 15
		return len(chk(10**(d - 1), 10**d))

	lenOfEachGroup = lenFrom(groupSize, d)
	extraAtBegin = lenOfEachGroup - lenFrom(groupSize - skipAtBegin, d) # will equal len(chk(first, first + skipAtBegin))
	extraAtEnd = lenFrom(skipAtEnd, d) # will equal len(chk(last - skipAtEnd, last))

	return extraAtBegin + extraAtEnd + groups * lenOfEachGroup

@functools.lru_cache(maxsize=None)
def cumulativeLenForDigits(d):
	if d < 1:
		raise Exception("negative")
	if d == 1:
		return lenForDigits(d)
	return lenForDigits(d) + cumulativeLenForDigits(d - 1)

def extractDigit(groupStart, indexIntoGroup, d):
	lo = 0 # incl
	hi = groupSize # excl
	while lo < hi - 1:
		mid = (lo + hi) // 2
		midStartsAt = lenFrom(mid, d)
		if indexIntoGroup < midStartsAt:
			hi = mid
		else:
			lo = mid
	if lo != hi - 1:
		raise Exception("oops")
	if indexIntoGroup == lenFrom(lo + 1, d) - 1:
		return "\n"
	indexIntoGroup -= lenFrom(lo, d)
	if charsFor[lo]:
		return charsFor[lo][indexIntoGroup]
	else:
		return str(groupStart + lo)[indexIntoGroup]

def calcIdx(idx):
	d = 1
	while cumulativeLenForDigits(d) <= idx:
		d += 1
	if d > 1:
		idx -= cumulativeLenForDigits(d - 1)
	# we want a character from the range of fizzbuzz where "d"-digit numbers are being printed
	skipAtBegin, skipAtEnd, groups, ignored, first = precomputedDataForDigits(d)
	lenOfEachGroup = lenFrom(groupSize, d)
	extraAtBeginLen = lenOfEachGroup - lenFrom(groupSize - skipAtBegin, d)
	extraAtEndLen = lenFrom(skipAtEnd, d)
	if idx < extraAtBeginLen:
		return chk(first, first + skipAtBegin)[idx]
	if idx >= lenForDigits(d) - extraAtEndLen:
		return chk(first * 10 - skipAtEnd, first * 10)[idx - (lenForDigits(d) - extraAtEndLen)]
	lenOfEachGroup = lenFrom(groupSize, d)
	idx -= extraAtBeginLen
	whichGroup, indexIntoGroup = divmod(idx, lenOfEachGroup)
	groupStart = first + skipAtBegin + whichGroup * groupSize
	return extractDigit(groupStart, indexIntoGroup, d)

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
