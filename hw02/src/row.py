import math
import utils

class ROW:
    def __init__(self, t):
        self.cells = t

    def like(self, data, n, nHypotheses):
        prior = (len(data.rows) + utils.THE_K) / (n + utils.THE_K * nHypotheses)
        out = math.log(prior)
        
        for col in data.cols.x:
            v = self.cells[col.at]
            if v != "?":
                inc = col.like(v, prior)
                out += math.log(inc)

        return math.exp(out)
    
    def likes(self, datas):
        n, nHypotheses = 0, 0

        for data in datas:
            n += len(data.rows)
            nHypotheses += 1

        most, out = None, None

        for k, data in enumerate(datas):
            tmp = self.like(data, n, nHypotheses)
            if most is None or tmp > most:
                most, out = tmp, k

        return out, most