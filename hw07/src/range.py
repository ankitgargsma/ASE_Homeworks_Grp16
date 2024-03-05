import math
import utils
from utils import *

class Range:
    def __init__(self, at, txt, lo, hi=None):
        self.at = at
        self.txt = txt
        self.scored = 0
        self.x = {'lo': lo, 'hi': hi or lo}
        self.y = {}

    def __str__(self):
        return "{{at: {}, scored: {}, txt: '{}', x: {{hi: {}, lo: {}}}, y: {{{}}}}}".format(
            self.at, self.scored, self.txt, self.x['hi'], self.x['lo'],
            ', '.join('{}: {}'.format(k, v) for k, v in self.y.items()))

    def add(self, x, y):
        self.x['lo'] = min(self.x['lo'], x)
        self.x['hi'] = max(self.x['hi'], x)
        self.y[y] = self.y.get(y, 0) + 1

    def show(self):
        lo, hi, s = self.x['lo'], self.x['hi'], self.txt
        if lo == -math.inf:
            return "{} < {}".format(s, hi)
        elif hi == math.inf:
            return "{} >= {}".format(s, lo)
        elif lo == hi:
            return "{} == {}".format(s, lo)
        else:
            return "{} <= {} < {}".format(lo, s, hi)

    def score(self, goal, LIKE, HATE):
        return utils.score(self.y, goal, LIKE, HATE)

    def merge(self, other):
        both = Range(self.at, self.txt, self.x['lo'])
        both.x['lo'] = min(self.x['lo'], other.x['lo'])
        both.x['hi'] = max(self.x['hi'], other.x['hi'])
        for t in [self.y, other.y]:
            for k, v in t.items():
                both.y[k] = both.y.get(k, 0) + v
        return both

    def merged(self, other, tooFew):
        both = self.merge(other)
        e1, n1 = utils.entropy(self.y)
        e2, n2 = utils.entropy(other.y)
        if n1 <= tooFew or n2 <= tooFew:
            return both
        if utils.entropy(both.y)[0] <= (n1 * e1 + n2 * e2) / (n1 + n2):
            return both

def ranges1(col, rowss):
    out = {}
    nrows = 0
    for y, rows in rowss.items():
        nrows += len(rows)
        for row in list(rows):
            x = row.cells[col.at]
            if x != "?":
                bin = col.bin(x)
                if bin not in out:
                    out[bin] = Range(col.at, col.txt, x)
                out[bin].add(x, y)
    out = list(out.values())
    out.sort(key=lambda a: a.x['lo'])
    return out if hasattr(col, 'has') else _mergeds(out, nrows / THE_BINS)

def _mergeds(ranges, too_few):
    t = []
    i=1
    while i <= len(ranges):
        a = ranges[i - 1]
        if i < len(ranges):
            both = a.merged(ranges[i], too_few)
            if both:
                a = both
                i += 1
        t.append(a)
        i += 1
    if len(t) < len(ranges):
        return _mergeds(t, too_few)
    for i in range(1, len(t)):
        t[i].x['lo'] = t[i - 1].x['hi']
    t[0].x['lo'] = -math.inf
    t[-1].x['hi'] = math.inf
    return t 
