import math
import utils
from config import *

class ROW:
    def __init__(self, t):
        self.cells = t

    def like(self, data, n, n_hypotheses):
        prior = (len(data.rows) + the['k']) / (n + the['k'] * n_hypotheses)
        out = math.log(prior)
        
        for col in data.cols.x:
            v = self.cells[col.at]
            if v != "?":
                inc = col.like(v, prior)
                out += math.log(inc)

        return math.exp(out)
    
    '''def likes(self, datas):
        n, nHypotheses = 0, 0

        for data in datas:
            n += len(data.rows)
            nHypotheses += 1

        most, out = None, None

        for k, data in enumerate(datas):
            tmp = self.like(data, n, nHypotheses)
            if most is None or tmp > most:
                most, out = tmp, k

        return out, most'''
    
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
        d, n = 0, 0
        for col in data.cols.y:
            n += 1
            d += (abs(col.heaven - col.norm(self.cells[col.at])) ** 2)
        return (d ** 0.5) / (n ** 0.5)