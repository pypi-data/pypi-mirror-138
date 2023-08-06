import random
import time
import json
import math
import sys

# CONSTANTS
Phi = (1 + math.sqrt(5)) / 2

def runtime(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        extension = "seconds"
        length = (end - start)
        if (length < 1):
            extension = "milliseconds"
            length *= 1000
        elif (length > 60):
            extension = "minutes"
            length /= 60
        
        print('{} runtime: {:.4f} {}'.format(
            func.__name__, length, extension
        ))
        return result
    
    return wrapper

def encrypt(txt: str, key:int=0) -> str:
    """
    simple encryption
    :param txt:
    :param key:
    :return:
    """
    if len(txt) == 0:
        return ''
    code = list(map(lambda c: c + '0' if len(c) < 3 else c, [str(ord(c) + key) for c in txt]))
    return hex(int(bin(int(''.join(code))), 2))[2:]

group = lambda x, n: [x[i:i + n] for i in range(0, len(x), n)]

def decrypt(text: str, k: int = 0) -> str:
    g = list(map(lambda n: n[:2] if int(n[0]) > 2 else n, group(str(int('0x' + text, 16)), 3)))
    return ''.join([chr(int(x) - k) for x in g])


def is_int(x) -> bool:
    try:
        int(x)
        return True
    except ValueError:
        return False

def is_whole_num(n) -> bool:
    return n % 1 == 0

def get_int(query: str) -> int:
    ans = input(query)
    while (not __isint(ans)):
        print("please enter an integer.")
        ans = input(query)
    return int(ans)


def get_int_with_params(query: str, bounds: list) -> int:
    ans = input(query)
    while (not is_int(ans)) and (ans not in bounds):
        print("invalid entry")
        ans = input(query)
    return int(ans)


def get_str_with_params(query: str, params: list) -> str:
    ans : str = input(query)
    while ans not in params:
        print("invalid entry")
        ans = input(query)
    return ans


def reverse_map(t: dict) -> dict:
    """
    return a reversed version of a dictionary
    where the keys are the values
    :param table:
    :return:
    """
    rev : dict = {}
    for key, val in t.items():
        rev[val] = key
    return t

str_to_list = lambda s: [c for c in s]

def fibeq(n) -> int:
    """
    return fibonaaci of a given number
    using the golden ratio equation
    Use case for when you want to calculate them
    faster than a recursive function would
    :param n:
    :return:
    """
    return math.floor((pow(Phi,n) - pow(1-Phi,n)) / math.sqrt(5))

def get_proper_divisors(n):
    factors = [1]
    for i in range(2, floor(sqrt(n))+1):
        if (n%i==0):
            factors.append(i)
            factors.append(n//i)
    return sorted(factors)



def fib(n: int) -> int:
    """ get fibonacci number"""
    def f(x, memo):
        if (x in memo): return memo[x]
        if x <= 1: return x
        memo[x] = f(x-1, memo) + f(x-2, memo)
        return memo[x]
    if n > 20:
        return f(n, {})
    else:
        return fibeq(n)

def fact(n) -> int:
    """get factorial of a number"""
    t = [i for i in range(n+1)]
    t[0] = 1
    for i in range(len(t)-1):
        t[i+1] = t[i]*(i+1)
    return t[n]

def is_prime(n):
    if n > 1:
        for i in range(2, (math.floor(math.sqrt(n))) + 1):
            if n % i == 0: return False
        return True
    return False


def get_primes(n):
    """
     generate a list of primes numbers up to a given limit
        using Sieve of Erasothenes
    """
    t = [True for i in range(n+1)]
    p = 2
    while ((p * p) <= n):
        if (t[p] == True):
            for j in range(p*p, n+1, p):
                t[j] = False
        p = p + 1
    return [i for i in range(len(t)) if t[i] != False][2:]


def get_factors(n: int, __numbers=None) -> list:
    """
    returns list of prime numbers
    that factor into a given number n
    in non-decreasing order
    """
    def f(x, nums, memo={}):
        if (x in memo): return memo[p]
        if (x == 1): return []
        if (not is_whole_num(x)): return None
        for num in nums:
            r = f(x / num, nums, memo)
            if (r != None):
                memo[n] = [num, *r]
                return memo[n]
        return None
    if (__numbers == None):
        __numbers = [i for i in range(2, n+1)]
    return f(n, __numbers)
    

def get_prime_factors(n: int) -> list:
    return get_factors(n, get_primes(n+1))


def gcd(x, y):
    """
    Euclid's algorithm for finding
    the greatest common divisor // Based
    off the theory/property that gcd(x,y) = gcd(y mod x, x)
    """
    if x >= 0 and y >= 0:
        if (y < x):
            y, x = x, y
        r = y % x
        
        while r != 0:
            y = x
            x = r
            r = y % x
        
        return x
    
    raise Exception("x and y must be positive integers")

def mul_inverse(x, n):
    """
    Finds inverse mod n of an integer x
    sx mod n = 1
    return None if x does not have an inverse mod n
    """
    if gcd(x,n) == 1:
        for s in range(1, n):
            if (s*x) % n == 1:
                return s
    return None

def lcm(x,y):
    """
    lowest common multiple of two numbers
    """
    return (x*y) // gcd(x, y)


def jprint(data: dict) -> None:
    print(json.dumps(data, indent=4))

def digitarray(n):
    """
    converts a number into a list of which
    each element is a digit of the number in order
    :param n: a number
    :return:
    """
    return [int(e) for e in str(n)]

def memset(a, val, size):
    for i in range(size):
        a[i] = val

def permutations(obj: [list, str, int]) -> list:
    """
    generate permutations of a list or string
    :param obj: list or str
    :return:list of permutations
    """
    t = type(obj)
    if not isinstance(t, list):
        if (isinstance(t, set)):
            raise Exception("argument must be list or string")
        elif t == str:
            obj = [e for e in obj]
        elif t == int:
            obj = digitarray(obj)
    
    def f(n, perms, curr=None, memo={}):
        if len(n) == 0:
            perms.append(curr)
        else:
            for i in range(len(n)):
                result = f(n[:i] + n[i + 1:], perms, curr + [n[i]])
            return perms
    
    result = f(obj, [], [])
    
    if (t == str):
        return [''.join(e) for e in result]
    elif (t == int):
        return [int(''.join(str(i) for i in e)) for e in result]
    return result


def count_subsets(n, r):
    return int(fact(n) / (fact(r) * fact(n - r)))


def combinations(obj: [list, str], r) -> list:
    """
    generate r-combinations of a given string
    or list and returns a list of those
    combinations
    :param obj:
    :param r:
    :return:
    """
    t = type(obj)
    c = [[] for i in range(count_subsets(len(obj), r))]
    def C(o, combs, curr=None):
        if (len(o) == len(obj) - r):
            if tuple(sorted(curr)) not in combs:
                combs.add(tuple(curr))
        else:
            for i in range(len(o)):
                result = C(o[:i] + o[i + 1:], combs, curr + [o[i]])
            return combs
        
    result = list(C(obj, set(), []))
    if (t == str):
        return sorted([''.join(e) for e in result])
    elif (t == list):
        return sorted(result)
    

# STRING CUSTOMIZATION
def bold(text):
    return f"\033[1m{text}\033[0m"

def add_color(text, color, background=False):
    COLORS = {
        "black": 30, "red": 31, "green": 32,
        "yellow": 33, "blue": 34, "purple": 35,
        "cyan": 36, "white": 37
    }
    if (background):
        for c in COLORS:
            COLORS[c] += 10
    
    return f"\u001b[{COLORS[color]}m{text}\u001b[0m"

def underline(text):
    return f"\u001b[4m{text}\u001b[0m"

def decorate(text, undline=False, makebold=False):
    if (undline):
        text = underline(text)
    if (makebold):
        text = bold(text)
    return text

def progress(func, calls: list):
    """
    track progress of
    :param func:
    :param args:
    :return:
    """
    for i in range(0, len(calls)):
        func(*calls[i])
        sys.stdout.write(u"\u001b[1000D" + str(round((i+1)/len(calls)*100)) + "%")
        sys.stdout.flush()
    print()

def is_palidrome(arg):
    if not isinstance(arg, str):
        arg = str(arg)
    stack = str_to_list(arg)
    while (len(stack) > 1):
        f = stack[0]
        stack = stack[1:]
        b = stack.pop()
        if (f != b):
            return False
    return True
