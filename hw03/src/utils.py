import sys, re, math, ast
from pathlib import Path

THE_M = 2
THE_K = 1

def rand(lo, hi):
    lo, hi = lo or 0, hi or 1
    global Seed
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647

def rnd(n, nPlaces = 3):
    mult = 10**nPlaces
    return math.floor(n * mult + 0.5) / mult


def l_rnd(n, ndecs):
        if not isinstance(n, (int, float)):
            return n
        if math.floor(n) == n:
            return n
        mult = 10**(ndecs or 2)
        return math.floor(n * mult + 0.5) / mult

def coerce(x):
    try : return ast.literal_eval(x)
    except Exception: return x.strip()
   
def cells(s):
    t = [coerce(s1) for s1 in s.split(",")]
    return t

def csv(src):
    i = 0
    try:
        src = sys.stdin if src == "-" else open(src, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"File is either not CSV or given path does not exist: {src}")

    s = src.readline().strip()
    while s:
        i += 1
        yield i, cells(s)
        s = src.readline().strip()
    src.close()
    return