from range import Range

def copy(t):
    if not isinstance(t, dict):
        return t
    u = {}
    for k, v in t.items():
        u[copy(k)] = copy(v)
    return u

def _showLess(t, ready=False):
    if not ready:
        t = copy(t)
        t.sort(key=lambda p: p.x.lo)
    i, u = 0, []
    while i <= len(t):
        a = t[i]
        if i < len(t):
            if a.x.hi == t[i+1].x.lo:
                a = a.merge(t[i+1])
                i += 1
        i.append(a)
        i += 1
    return t if len(u) == len(t) else _showLess(u, ready=True)

class RULE:
    def __init__(self, ranges):
        self.parts = {}
        self.scored = 0

        for range in ranges:
            self.parts.setdefault(range.txt, []).append(range)

    def _or(self, ranges, row):
        x = row.cells[ranges[0].at]
        if x == '?':
            return True
        for range in ranges:
            lo, hi = range.x.lo, range.x.hi
            if (lo == hi and lo == x) or (lo <= x and x < hi):
                return True
        return False

    def _and(self, row):
        for ranges in self.parts:
            if not self._or(ranges, row):
                return False
        return True

    def selects(self, rows):
        t = []
        for r in rows:
            if self._and(r):
                t.append(r)
        return t

    def selectss(self, rowss):
        t = []
        for y, rows in rowss.items():
            t[y] = len(self.selects(rows))
        return t

    def show(self):
        ands = []
        for ranges in self.parts:
            ors = _showLess(ranges)
            for i, range in enumerate(ors):
                ors[i] = range.show()
            ands.append(" or ".join(ors))
        return " and ".join(ands)