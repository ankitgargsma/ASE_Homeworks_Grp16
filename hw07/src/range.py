import math
import utils

class Range:
    def __init__(self, at, txt, lo):
        self.at = at
        self.txt = txt
        self.scored = 0
        self.x = {'lo': lo, 'hi': lo}
        self.y = {}

    def add(self, x, y):
        self.x["lo"] = min(self.x["lo"], x)
        self.x["hi"] = max(self.x["hi"], x)
        self.y[y] = self.y.get(y, 0) + 1

    def show(self):
        lo, hi, s = self.x["lo"], self.x["hi"], self.txt
        if lo == -math.inf:
            return f"{s} < {hi}"
        if hi == math.inf:
            return f"{s} >= {lo}"
        if lo == hi:
            return f"{s} == {lo}"
        return f"{lo} <= {s} < {hi}"

    def score(self, goal, LIKE, HATE):
        return utils.score(self.y, goal, LIKE, HATE)

    def merge(self, other):
        both = Range(self.at, self.txt, self.x["lo"])
        both.x["lo"] = min(self.x["lo"], other.x["lo"])
        both.x["hi"] = max(self.x["hi"], other.x["hi"])
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
        if utils.entropy(both.y) <= (n1 * e1 + n2 * e2) / (n1 + n2):
            return both

def ranges(cols, rowss):
        t = []
        for col in cols:
            for range_ in ranges1(col, rowss):
                t.append(range_)
        return t

def ranges1(col, rowss):
        out = {}
        nrows = 0
        for y, rows in rowss.items():
            nrows += len(rows)
            for row in rows:
                x = row.cells[col.at]
                if x != "?":
                    bin_ = col.bin(x)
                    if bin_ not in out:
                        out[bin_] = Range(col.at, col.txt, x)
                    out[bin_].add(x, y)
        out = utils.asList(out)
        out.sort(key=lambda range_: range_.x["lo"])
        return out if col.has else _mergeds(out, nrows / utils.THE_BINS)


def _mergeds(ranges, tooFew):
        i = 1
        t = []
        while i <= len(ranges):
            a = ranges[i - 1]
            if i < len(ranges):
                both = a.merged(ranges[i], tooFew)
                if both:
                    a = both
                    i += 1
            t.append(a)
            i += 1

        if len(t) < len(ranges):
            return _mergeds(t, tooFew)

        for i in range(1, len(t)):
            t[i].x.lo = t[i - 1].x.hi

        t[0].x.lo = -math.inf
        t[-1].x.hi = math.inf
        return t

