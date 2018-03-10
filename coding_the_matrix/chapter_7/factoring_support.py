from math import sqrt
from functools import reduce
import operator

def gcd(x,y): return x if y == 0 else gcd(y, x % y)

def dumb_factor(x, primeset):
    """ If x can be factored over the primeset, return the
    set of pairs (p_i, a_i) such that x is the product
    of p_i to the power of a_i.
    If not, return []
    """
    factors = []
    for p in primeset:
        exponent = 0
        while x % p == 0:
            exponent = exponent + 1
            x = x//p
        if exponent > 0:
            factors.append((p,exponent))
    return factors if x == 1 else []

def primes(limit):
    primeset = set()
    a = [True] * limit # Initialize the primality list
    a[0] = a[1] = False
    for (i, isprime) in enumerate(a):
        if isprime:
            primeset.add(i)
            for n in range(i*i, limit, i): # Mark factors non-prime
                a[n] = False
    return primeset

def intsqrt(x):
    L = 1
    H = x
    if H<L: L, H = H, L
    while H - L > 1:
        m = int((L+H)//2)
        d = x//m
        if d > m: L = m
        else: H = m
    return L if L*L == x else H

def prod(factors):
    "return product of numbers in given list"
    return reduce(operator.mul, factors, 1)
