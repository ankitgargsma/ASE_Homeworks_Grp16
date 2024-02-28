import math
from utils import *
from config import *

class ROW:
    def __init__(self, t):
        self.cells = t

    def like(self, data, n, nHypothesis):
        #k = config.value.k
        k = the['k']
        prior = (len(data.rows) + k) / (n + k * nHypothesis)
        out = math.log(prior)
        for col in data.cols.x:
            v = self.cells[col.at]
            if v != "?":
                inc = col.like(v, prior)
                try:
                    out += math.log(inc)
                except:
                    return float("-inf")
        return math.exp(out)
    
    def likes(self, datas):
        n, n_hypotheses = 0, 0

        for k, data in datas.items():
            n += len(data.rows)
            n_hypotheses += 1
        
        most, out = None, None

        for k, data in datas.items():
            tmp = self.like(data, n, n_hypotheses)
            if most is None or tmp > most:
                most, out = tmp, k

        return out, most
    
    def d2h(self, data):
        d, n, p = 0, 0, 2
        for col in data.cols.y:
            n += 1
            d += abs(col.heaven - col.norm(self.cells[col.at])) ** p
        return (d / n) ** (1 / p)
    
    def dist(self, other, data, d=0, n=0):
        d, n, p = 0, 0, 2
        for col in data.cols.x:
            n += 1
            d += col.dist(self.cells[col.at], other.cells[col.at]) ** p
        return (d / n) ** (1 / p)

    def neighbors(self, data, rows=None):
        return keysort(rows or data.rows, lambda row: self.dist(row, data))