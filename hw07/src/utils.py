import sys, re, math, ast
from pathlib import Path
import random, time

THE_M = 2
THE_K = 1
THE_FAR = .95
THE_P = 2
THE_BINS = 16
THE_SUPPORT = 2
THE_BEAM = 10
THE_COHEN = .35
THE_CUT = .1
THE_SEED = 31210
THE_d = 32
THE_D = 4
THE_HALF = 256

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

def coerce(s):
    def coerce_helper(s2):
        return None if s2 == "null" else s2.lower() == "true" or (s2.lower() != "false" and s2)
    try:
        return float(s) if s is not None else None
    except ValueError:
        return coerce_helper(re.match(r'^\s*(.*\S)', s).group(1)) if isinstance(s, str) else s

def output(x):
    items = ", ".join([f"{k}: {v}" for k, v in sorted(x.items()) if k[0] != "_"])
    return f"{{{items}}}"

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

def settings(s):
    t = {}
    opt_dir = {}
    opts = re.findall(r'-(\w+)\s+--(\w+)\s+.*=\s*(\S+)', s)
    for short_form, full_form, default_value in opts:
        t[full_form] = coerce(default_value)
        opt_dir[short_form] = full_form

    options = sys.argv[1:]
    if "--help" in options or "-h" in options:
        t["help"] = True
        return t

    options_dict = {}
    for i in range(0, len(options), 2):
        opt = options[i]
        val = options[i + 1] if i + 1 < len(options) else None
        options_dict[opt] = val

    for opt, val in options_dict.items():
        key = opt[2:] if opt.startswith('--') else opt_dir[opt[1:]]
        t[key] = coerce(val)

    return t

def slice(t: list, go: int = None, stop: int = None, inc: int = None) -> list:
    go = go or 0
    stop = stop or len(t)
    inc = inc or 1

    if go < 0:
        go += len(t)
    if stop < 0:
        stop += len(t)

    return t[go:stop:inc]

def set_random_seed():
        seed = int(re.sub(r'[^0-9]', '', str(time.time())[-7:]))
        return seed

def any(t):
    return random.choice(t)

def score(t, goal, LIKE, HATE, tiny=1E-30):
    like, hate = 0, 0
    for klass, n in t.items():
        if klass == goal:
            like += n
        else:
            hate += n
    like = like / (LIKE + tiny)
    hate = hate / (HATE + tiny)
    if hate > like:
        return 0
    else:
        return like ** THE_SUPPORT / (like + hate)
    
def entropy(t):
    n = sum(t.values())
    e = 0
    for v in t.values():
        e -= (v / n) * math.log(v / n, 2)
    return e, n

def asList(t):
    u = []
    for v in t:
        u.append(t[v])
    return u

def copy(t):
    if not isinstance(t, dict):
        return t
    
    u = {}
    for k, v in t.items():
        u[copy(k)] = copy(v)
    return u

def powerset(s):
    t = [[]]
    for i in range(len(s)):
        for j in range(len(t)):
            t.append([s[i]] + t[j])
    return t