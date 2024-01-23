import math

class NUM:
    def __init__(self, s, n):
        if( s is None):
            self.s = " "
        else:
            self.s = s
        if( n is None):
            self.at = 0
        else:
            self.at = n
        self.txt = s
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.hi = float('-inf')
        self.lo = float('inf')
        if s[-1] == '-':
            self.heaven = 0
        else:
            self.heaven = 1
        
        self.w = -1 if "-" in self.txt else 1
    def add(self, x):
        if(x != "?"):
            self.n = self.n + 1
            d = x - self.mu
            self.mu = self.mu + d/self.n
            self.m2  =self.m2 + d*(x - self.mu)
            self.lo =  min(x, self.lo)
            self.hi = max(x, self.hi)
        return self

    def mid(self):
        return self.mu
    
    #Calculates standard deviation
    def div(self):
        if self.n < 2:
            return 0
        return (self.m2/(self.n - 1))**.5
    
    #Normalization based on low and high values
    def norm(self,x):
        if x == "?":
            return x
        return (x - self.lo)/(self.hi - self.lo + float("-inf"))
    
    def like(self, x, prior):
        mu, sd = self.mid(), (self.div() + 1E-30)
        nom = math.exp(-0.5 * ((x - mu) ** 2) / (sd ** 2))
        denom = (sd * 2.5 + 1E-30)
        return nom / denom