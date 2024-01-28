from row import ROW
from cols import COLS
from sym import SYM
from num import NUM
from utils import *;

class DATA:
    def __init__(self, src=[], fun=None):
        self.rows = []
        self.cols = None
        if isinstance(src, str):
            for _, x in csv(src):
                self.add(x, fun)
        else:
            #for _, x in enumerate(src):
            self.add(src, fun)

    def add(self, t, fun=None):
        row = ROW(t) if type(t) == list else t
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)

    def mid(self, cols=None):
        u = [col.mid() for col in (cols or self.cols.all)]
        return ROW.new(u)
    
    def stats(data):
        Stats = {}
        row_count = max(col.n for col in data.cols.all)
        Stats[".N"] = row_count
        for col in data.cols.all:
            if isinstance(col, NUM):
                mean = col.mid()
                Stats[f"{col.txt}"] = round(mean, 2)
            elif isinstance(col, SYM):
                mode = col.mid()
                Stats[f"{col.txt}"] = mode

        return Stats
    
    def bestRest(self,rows, want):
        rows.sort(key=lambda row: self.d2h(row))

        # Initialize best and rest lists with column names
        best, rest = [self.cols.names], [self.cols.names]

        # Split rows into best and rest
        for i, row in enumerate(rows, 1):
            if i <= want:
                best.append(row)
            else:
                rest.append(row)

    def split(self, best, rest, lite, dark):
        selected = DATA([self.cols.names])
        max_val = 1E30
        out = 1

        for i, row in enumerate(dark, 1):
            b = row.like(best, len(lite), 2)
            r = row.like(rest, len(lite), 2)
            
            if b > r:
                selected.add(row)
            
            tmp = abs(b + r) / abs(b - r + 1E-300)
            if tmp > max_val:
                out, max_val = i, tmp

        return out, selected
