import math
from sym import SYM
from num import NUM

class COLS:
    def __init__(self, t):
        self.names = t
        self.all = []
        self.x = []
        self.y = []
        self.klass = None

        for txt in t:
            if txt[0].isupper():
                col = NUM(t.index(txt), txt)
            else:
                col = SYM(t.index(txt), txt)
            self.all.append(col)

            if not txt[-1] == "X":
                if "-" in txt or "+" in txt or "!" in txt:
                    self.y.append(col)
                else:
                    self.x.append(col)
                if "!" in txt:
                    self.klass=col

    def add(self, row):
        for cols in [self.x, self.y]:
            for col in cols:
                col.add(row.cells[col.at])
