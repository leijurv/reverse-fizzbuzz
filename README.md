# Reverse FizzBuzz

Some people attempt to compute the `n`th digit of Pi, where `n` is some huge number. For example, a little while ago Google calculated the 100 trillionth digit of Pi (aka: 10^18). This is the same idea: compute the `n`th character of FizzBuzz, where `n` is huge. But when **I** say "huge" **I** don't mean 10^18, I mean 10^10000000000, like I literally mean "1" with ten billion "0"s after it.

See the following example cases:

| `idx`  | `ReverseFizzBuzz(idx)` should equal |
| - | - |
| 0 | `"1"` |
| 1 | `"\n"` |
| 2 | `"2"` |
| 3 | `"\n"` |
| 4 | `"F"` |
| 5 | `"i"` |
| 6 | `"z"` |
| 7 | `"z"` |
| 8 | `"\n"` |
| 9 | `"4"` |
| 10^1 | `"\n"` |
| 10^10 | `"5"` |
| 10^100 | `"0"` |
| 10^1000 | `"F"` |
| 10^10000 | `"6"` |
| 10^100000 | `"0"` |
| 10^1000000 | `"7"` |
| 10^10000000 | `"7"` |
| 10^100000000 | `"9"` |
| 10^1000000000 | `"3"` |
| 10^10000000000 | `"1"` |

With this repo, you can compute amazing facts like that ^ in a performant manner!

Time to calculate those last few rows on my laptop:

| `idx`  | `ReverseFizzBuzz(idx)` should equal | Time in `fizzbuzz_optim_optim.py` | Time in `fizzbuzz.nb` |
| - | - | - | - |
| 10^1000000 | `"7"` | Five seconds | 0.04 seconds |
| 10^10000000 | `"7"` | Four minutes | 0.4 seconds |
| 10^100000000 | `"9"` | Seven hours | Five seconds |
| 10^1000000000 | `"3"` | ? | 70 seconds
| 10^10000000000 | `"1"` | ? | 13 minutes (and 43 gigabytes of RAM) |


**Open challenge: try and compute ReverseFizzBuzz(10^10^11)!** The table must grow.

## Normal FizzBuzz

Print out the integers, starting at 1. For any that are divisible by three, instead print "Fizz". For any that are divisible by five, instead print "Buzz". For any that are divisible by both three and five, instead print "FizzBuzz".

FizzBuzz looks like:

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
```

et cetera...

## This repo

The simplest possible implementation actually generates the FizzBuzz string up to the desired index, then returns the relevant character. I didn't write that one since it's boring and slow.

`fizzbuzz.py` is the initial version and it's fairly simple (80 lines of code including comments and blanks). The `ReverseFizzBuzz` function is called `calcIdx`. On my desktop, it does `calcIdx(2**10000)` in about 1.1 seconds, and `calcIdx(2**20000)` in about 7.8 seconds. It's a bit tricky because each FizzBuzz group changes in length as the number of digits in the numbers goes up. For example, the length in characters of the 1-digit numbers is 30, then 378 for 2-digit, then 4260 for 3-digit, then 47400 for 4-digit, etc. (foreshadowing: the hard part will end up being just figuring out what digit length numbers we're printing as of a given index)

`fizzbuzzpop.py` extends the idea to any kind of FizzBuzz. For example, you could add in that any numbers divisible by 7 are "Pop" by uncommenting the relevant line at the top.

`fizzbuzz_optim.py` is the first version that's optimized for performance, while still being written generally for any FizzBuzzPop, and without becoming TOO complicated (145 lines of code including comments and blanks). This optimization was very interesting, for example I've never before had to cache simple arithmetic operations such as addition, but that's what happens when your integers are tens to hundreds of thousands of bits long. (edit: deleted some now-irrelevant discussion here, since this file is no longer my state of the art, and the next file now implements every optimization idea I previously had listed in the readme). The highest I've been able to go with this version was `ReverseFizzBuzz(10^10^6) = "7"`, taking about five minutes and needing a lot of RAM.

`fizzbuzz_optim_optim.py` is the version that's specialized for just FizzBuzz (no Pop). Specifically, it takes advantage of one beautiful fact: consider the two-digit numbers (10 through 99). There are 90 of them. *That's divisible by 15*, so the FizzBuzz pattern repeats an integer number of times. Same goes for three digit numbers (100 through 999), there are 900 of them, which is divisible by 15. Generally, `10^n - 10^(n-1)` is always divisible by 15. This allows us to do some very fast optimizations: every group of FizzBuzz for d-digit numbers has total length easily computable as `10**(d-2) * (48 * d + 282)`, and even better, we can compute a closed form of this summation (thanks WolframAlpha) as `((415 + 72 * d) * 10**d - 820) // 135`, then binary search on that to compute what digit length of FizzBuzz is currently being printed for any index in log log log time (yes I do mean triple log, see the comments around `binarySearchBitLens`). This version took `ReverseFizzBuzz(10^10^6)` down from five minutes to five seconds, and made possible the next few rows of the table up top.

Finally, I took all the learnings from `fizzbuzz_optim_optim.py` and ported them to Mathematica because I suspected its extremely large precision integers would work well (I've used them before). I was correct, and `ReverzeFizzBuzz(10^10^8)` took seven hours in `fizzbuzz_optim_optim.py` but only five seconds in Mathematica. I used it to compute `ReverzeFizzBuzz(10^10^9)` and `ReverzeFizzBuzz(10^10^10)`.

## Benchmark

If you run them (Python 3.9+ required), you'll see that they do a verification routine, then a benchmark routine. The verification is generating 1234567 lines of FizzBuzz, then testing the first 10000 characters, as well as a random selection of 10000 more characters. The benchmark is printing out every power of 2 index of FizzBuzz, up to 2^20000.

| File | Time to perform this benchmark (on my laptop) |
| - | - |
| `fizzbuzz.py` | ~75 seconds |
| `fizzbuzzpop.py` | ~85 seconds |
| `fizzbuzz_optim.py` | ~7.5 seconds |
| `fizzbuzz_optim_optim.py` | ~1.36 seconds |

The stdout of running any of the four should be the same.

`fizzbuzz_optim_optim.py` then shows off by doing some stuff that the other versions can't do (but this showoff stuff goes to stderr so as not to mess up the shasum).

The output should be:

```
Verified
Character 2^0 of FizzBuzz is 

Character 2^1 of FizzBuzz is 2
Character 2^2 of FizzBuzz is F
Character 2^3 of FizzBuzz is 

Character 2^4 of FizzBuzz is F
Character 2^5 of FizzBuzz is z
Character 2^6 of FizzBuzz is F
Character 2^7 of FizzBuzz is i
Character 2^8 of FizzBuzz is z
Character 2^9 of FizzBuzz is 1
Character 2^10 of FizzBuzz is B
Character 2^11 of FizzBuzz is 6
Character 2^12 of FizzBuzz is i
Character 2^13 of FizzBuzz is 

Character 2^14 of FizzBuzz is 

Character 2^15 of FizzBuzz is u
Character 2^16 of FizzBuzz is 1
Character 2^17 of FizzBuzz is 2
Character 2^18 of FizzBuzz is 9
Character 2^19 of FizzBuzz is 1
Character 2^20 of FizzBuzz is 4
Character 2^21 of FizzBuzz is 8
Character 2^22 of FizzBuzz is F
Character 2^23 of FizzBuzz is 0
Character 2^24 of FizzBuzz is 4
```

...

```
Character 2^19990 of FizzBuzz is 7
Character 2^19991 of FizzBuzz is 7
Character 2^19992 of FizzBuzz is 1
Character 2^19993 of FizzBuzz is 0
Character 2^19994 of FizzBuzz is 2
Character 2^19995 of FizzBuzz is 3
Character 2^19996 of FizzBuzz is 5
Character 2^19997 of FizzBuzz is 7
Character 2^19998 of FizzBuzz is 0
Character 2^19999 of FizzBuzz is 3
```

Piping the output to `shasum` should yield `7cbcd72e6c37e26435f7ba85c6a51306cc1eec82`.


## The Mathematica code
`fizzbuzz.nb` is impossible to read without Mathematica, so I'll paste the main here as convenience / for curiosity.

```
CumulativeLen[d_] := 
 Block[{}, If[d < 1, Print["won't be right"]]; 
  If[d == 1, 30, Quotient[(415 + 72*d)*10^d - 820, 135]]]; hardcoded =
  Characters[
  "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\n"];(*the one-digit numbers \
are an exception because there are ten of them, which isn't divisible \
by 15. but the quantity of two digit numbers IS divisible by 15, as \
is the quantity of every subsequent digit length*)If[
 Length[hardcoded] != CumulativeLen[1], Print["bad data"]]; charsFor =
  Characters /@ {"Buzz", "", "Fizz", "", "", "FizzBuzz", "", "", 
   "Fizz", "", "Buzz", "Fizz", "", "", "Fizz"}; charsUpToIncl = {5, 6,
   11, 12, 13, 22, 23, 24, 29, 30, 35, 40, 41, 42, 
  47}; numsUpToIncl = {0, 1, 1, 2, 3, 3, 4, 5, 5, 6, 6, 6, 7, 8, 8}; 
LenFrom[maxExcl_, d_] := 
 If[maxExcl == 0, 0, 
  charsUpToIncl[[maxExcl]] + numsUpToIncl[[maxExcl]]*d]; 
ExtractDigit[indexIntoGroup_, d_] := 
 Block[{lo}, lo = 0; 
  While[indexIntoGroup >= LenFrom[lo, d], lo = lo + 1]; lo - 1]; 
CalcDForIdx[idx_] := 
 Block[{d, lo, hi, mid}, lo = 1; hi = 1; 
  While[CumulativeLen[hi] <= idx, hi *= 2]; 
  While[lo < hi - 1, mid = Quotient[lo + hi, 2]; 
   If[CumulativeLen[mid] > idx, hi = mid, lo = mid]]; d = lo; 
  While[CumulativeLen[d] <= idx, d += 1]; d]; 
ReverseFizzBuzzKnowingDigitLength[idx_, d_] := 
 Block[{newIdx, lenOfEachGroup, qr, whichGroup, indexIntoGroup, 
   groupStart, actual, lo}, 
  If[idx < Length[hardcoded], Return[hardcoded[[idx + 1]]]];
  If[CumulativeLen[d] <= idx, Print["bad data (d is too low)"]; 
   Return[]];
  If[CumulativeLen[d - 1] > idx, Print["bad data (d is too high)"]; 
   Return[]];
  newIdx = idx - CumulativeLen[d - 1];
  lenOfEachGroup = LenFrom[15, d];
  qr = QuotientRemainder[newIdx, lenOfEachGroup];
  whichGroup = qr[[1]];
  indexIntoGroup = qr[[2]];
  groupStart = 10^(d - 1) + whichGroup*15;
  lo = ExtractDigit[indexIntoGroup, d];
  If[indexIntoGroup == LenFrom[lo + 1, d] - 1, Return["\n"]];
  indexIntoGroup = indexIntoGroup - LenFrom[lo, d];
  If[Length[charsFor[[lo + 1]]] > 0, 
   Return[charsFor[[lo + 1]][[indexIntoGroup + 1]]]];
  actual = groupStart + lo;
  Mod[Quotient[actual, 10^(d - indexIntoGroup - 1)], 10]
  ];
 ReverseFizzBuzz[idx_] := 
 ReverseFizzBuzzKnowingDigitLength[idx, CalcDForIdx[idx]]
 ```
