# Reverse FizzBuzz

Some people attempt to compute the `n`th digit of Pi, where `n` is some huge number. For example, a little while ago Google calculated the 100 trillionth digit of Pi (aka: 10^18). This is the same idea: compute the `n`th character of FizzBuzz, where `n` is huge. But when **I** say "huge" **I** don't mean 10^18, I mean 10^10000000, like I literally mean "1" with ten million "0"s after it.

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
| 10^100000000 | ? (my laptop has been running the final integer division to compute this one for the last 5+ hours) |

With this repo, you can compute amazing facts like that ^ in a performant manner! (`fizzbuzz_optim_optim.py` generates the above table roughly instantly, except the third to last row takes a little over five seconds, the second to last row takes a little under five minutes, and the last row took hours and still isn't done)


**Open challenge: try and compute ReverseFizzBuzz(10^10^8)!** My laptop may or may not finish it lol.

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
