import math
import utils

class SYM:
    def __init__(self, s=" ", n=0):
        self.txt = s
        self.at = n
        self.n = 0
        self.has = {}
        self.most = 0
        self.mode = None

    def add(self, x):
        if not x == "?":
            self.n +=1
            self.has[x]= 1 + (self.has[x] if x in self.has.keys() else 0)
            if self.has[x] > self.most:
                self.most = self.has[x]
                self.mode = x
    def mid(self):
        return self.mode

    def div(self):
        def fun(p):
            return p * math.log2(p)
        e = 0
        for _, n in self.has.items():
            e = e + fun(n/self.n)
        return -e

    def like(self, x, prior):
        return ((self.has.get(x, 0) or 0) + utils.THE_M * prior) / (self.n + utils.THE_M)
    
    def dist(self, x, y):
        return 1 if (x == "?" and y == "?") else (0 if x == y else 1)