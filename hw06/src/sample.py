import sys, random

class SAMPLE:
  def __init__(self,lst=[],txt="",rank=0):
    self.has = []
    self.ready = False
    self.txt = txt
    self.rank = 0
    self.n, self.sd, self.m2, self.mu = 0,0,0,0
    self.lo, self.hi = sys.maxsize, -sys.maxsize
    [self.add(x) for x in lst]

  def add(self,x):
    self.has += [x]; self.ready=False;
    self.lo = min(x,self.lo)
    self.hi = max(x,self.hi)
    self.n += 1
    delta = x - self.mu
    self.mu += delta / self.n
    self.m2 += delta * (x -  self.mu)
    self.sd = 0 if self.n < 2 else (self.m2 / (self.n - 1))**.5

  def ok(self):
    if not self.ready:
      self.has = sorted(self.has)
    self.ready=True
    return self

  def mid(self):
    has=self.ok().has
    return has[len(has)//2]

  def bar(self, num, fmt="%8.3f", word="%10s", width=50):
    out  = [' '] * width
    pos = lambda x: int(width * (x - self.lo) / (self.hi - self.lo + 1E-30))
    has = num.ok().has
    [a, b, c, d, e]  = [has[int(len(has)*x)] for x in [0.5,0.25,0.5,0.75,0.95]]
    [na,nb,nc,nd,ne] = [pos(x) for x in [a,b,c,d,e]]
    for i in range(nb,nd): out[i] = "-"
    out[width//2] = "|"
    out[nc] = "*"
    return ', '.join(["%2d" % num.rank, word % num.txt, fmt%c, fmt%(d-b),
            ''.join(out), fmt%self.lo, fmt%self.hi ])