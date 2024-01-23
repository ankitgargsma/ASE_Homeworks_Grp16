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