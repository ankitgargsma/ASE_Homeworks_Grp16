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
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.hi = float('-inf')
        self.lo = float('inf')
        if s[-1] == '-':
            self.heaven = 0
        else:
            self.heaven = 1

    def add(self, x, d):
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
    
    def norm(self,x):
        return x == "?" and x or (x - self.lo)/(self.hi - self.lo + float("-inf"))