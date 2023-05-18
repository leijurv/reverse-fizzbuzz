import time
start = time.time()
import functools
import random
import math
import sys
sys.set_int_max_str_digits(10**7)

@functools.lru_cache(maxsize=None)
def chk(minIncl, maxExcl):
	s = ""
	for i in range(minIncl, maxExcl):
		if i % 15 == 0:
			s += "FizzBuzz\n"
		elif i % 3 == 0:
			s += "Fizz\n"
		elif i % 5 == 0:
			s += "Buzz\n"
		else:
			s += str(i) + "\n"
	return s

def precomputeData():
	charsFor = [""] * 15
	for i in range(len(charsFor)):
		if i % 3 == 2: # <-- why == 2? because we are offseting all groups (starting with the two digit numbers) by +10 so that they start at 10, and this equates to (i+10)%3==0 the reason is that every power of ten (starting at ten) is ten more than a multiple of 15. (aka 100 is 90+10 with 90 divisible by 15, 1000 is 990+10 with 990 divisible by 15, etc)
			charsFor[i] += "Fizz"
		if i % 5 == 0: # not needed here because ten is divisible by five
			charsFor[i] += "Buzz"
	charsUpToIncl = []
	runningTot = 0
	numsUpToIncl = []
	numsTot = 0
	for i in range(len(charsFor)):
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

skipCaching = False # False means that it walks forwards by powers of ten. this is good/fast if you want to do the normal benchmark of 2^1 through 2^20000, but it's bad/slow if you want to immediately skip all the way up to 10^10000000 or something

@functools.lru_cache(maxsize=None)
def powerOfTen(d):
	# "you're silly, there's no way you need to cache powers of 10, and there's definitely no way it's faster to recursively multiply by ten rather than just returning 10**d"
	# you're wrong and i'm not silly, go ahead and try the benchmark with just "return 10**d" and/or without the cache
	if skipCaching:
		return 10**d # slower
	if d == 0:
		return 1
	return 10 * powerOfTen(d - 1)

@functools.lru_cache(maxsize=None)
def lenForDigits(d):
	# length of fizzbuzz for all numbers that are "d" decimal digits long
	if d == 1:
		return 30
	return powerOfTen(d - 2) * (48 * d + 282)

@functools.lru_cache(maxsize=None)
def cumulativeLenForDigits(d):
	if d < 1:
		raise Exception("negative")
	if d == 1:
		return lenForDigits(d)
	if skipCaching:
		# wolfram alpha gave this magical closed form for the summation, yay!
		# https://www.wolframalpha.com/input?i=30+%2B+sum+from+i%3D2+to+n+of+10%5E%28i-2%29*%2848*i%2B282%29

		# this isn't THAT much faster than cumulativeLenForDigitsOld **IF** the previous cumulativeLens have already been computed and cached
		# if you want one particular cumulativeLen that's way beyond what's previously been calculated, however, then this is much faster
		
		return ((415 + 72 * d) * powerOfTen(d) - 820) // 135
	return lenForDigits(d) + cumulativeLenForDigits(d - 1)

cachedBitLens = []
@functools.lru_cache(maxsize=None)
def bitLen(d):
	if skipCaching:
		#print("bitlen", d)
		return cumulativeLenForDigits(d).bit_length()
	global cachedBitLens
	while len(cachedBitLens) < d:
		cachedBitLens.append(cumulativeLenForDigits(len(cachedBitLens) + 1).bit_length())
	return cachedBitLens[d-1]

def extractDigit(groupStart, indexIntoGroup, d):
	lo = 0 # incl
	hi = 15 # excl
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
		actualNumberBeingPrinted = groupStart + lo
		digitExtraction = powerOfTen(d - indexIntoGroup - 1)
		leastSignificant = actualNumberBeingPrinted // digitExtraction # <-- this line takes most of the time lol
		return str(leastSignificant % 10)

# find minimum value thats greater or equal
@functools.lru_cache(maxsize=None)
def binarySearchBitLens(ln):
	lo = 0
	hi = len(cachedBitLens)
	if skipCaching:
		# the bit length of the requested fizzbuzz index (aka: the "ln" argument) gives precise upper and lower bounds on the log base 2 of the idx, we convert those to base 10 and use them to generate the upper and lower bounds for our binary search on how many digits of fizzbuzz we're currently outputting

		guess = int(ln * math.log(2) / math.log(10)) # so, ln is already O(log n), so this is as well, therefore guess.bit_length() is O(log log n)
		overshootApprox = int(math.ceil(guess.bit_length() * math.log(2) / math.log(10))) # <-- this is where the triple log comes from (the gap between lo and hi is overshootApprox which is O(log log n) therefore binary search between lo and hi takes O(log log log n) steps)

		startAt = guess - overshootApprox
		lo = startAt - 2 # these offsets (-2 and +1) are only needed for the first few thousand lines. after that, this process becomes more accurate as the effects of rounding to the nearest integer in the logs becomes negligible
		hi = guess + 1

	while lo < hi - 1:
		mid = (lo + hi) // 2
		if bitLen(mid + 1) >= ln:
			hi = mid
		else:
			lo = mid
	ret = lo + 1 # the index is d-1 because one-offset
	if bitLen(ret) >= ln:
		raise Exception("no") # guarantee 
	return ret

hardcoded = chk(1, 10) # one digit needs special case because 10^0 is 1 mod 15, but 10^x for all other x is 10 mod 15

def calcIdx(idx):
	if idx < len(hardcoded):
		return hardcoded[idx]

	# we want a character from the range of fizzbuzz where "d"-digit numbers are being printed
	# turns out that I found the hardest part to be figuring out "d" in a way that's efficient even when idx is more than 10^1000000

	d = 1
	idx_bit_len = idx.bit_length()

	if idx_bit_len > 5 and (cachedBitLens or skipCaching):
		d = binarySearchBitLens(idx_bit_len) # this looks stupid, but comment it out and the bench gets 2.5 seconds slower :)

	while bitLen(d) < idx_bit_len:
		d += 1

	while cumulativeLenForDigits(d) <= idx:
		d += 1
	if d > 1:
		idx -= cumulativeLenForDigits(d - 1)
		if idx < 0:
			# basically with this check, combined with the immediately previous while loop, it's guaranteed that no matter what the sketchy binary search does, it will fail here if "d" is too high, and the while loop will correct if "d" is too low
			raise Exception("picking length failed")

	first = powerOfTen(d - 1)
	lenOfEachGroup = lenFrom(15, d)
	whichGroup, indexIntoGroup = divmod(idx, lenOfEachGroup)
	groupStart = first + whichGroup * 15 # this is completely incorrect - it's always off by 10 (because 10^x mod 15 is 10), but, since we created our tables in precomputeData with a -10 offset, it ends up being correct lol
	return extractDigit(groupStart, indexIntoGroup, d)

if False:
	print(chk(1, 20))

if True: # verification routine
	random.seed(137)
	maxN = 1234567
	chkStr = chk(1, maxN)
	for i in range(10000):
		if chkStr[i] != calcIdx(i):
			raise Exception("wrong " + str(i) + " " + chkStr[i] + " " + calcIdx(i))
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
	chIdx = 1
	for i in range(20000):
		#print(i)
		c = calcIdx(chIdx)
		print("Character", "2^"+str(i), "of FizzBuzz is", c)
		verify += c
		chIdx = chIdx + chIdx
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

if True:
	skipCaching = True
	for i in range(7):
		print("10**"+str(10**i), "aka", "10**(10**" + str(i) + ")", file=sys.stderr)
		print(calcIdx(10**(10**i)), file=sys.stderr)
