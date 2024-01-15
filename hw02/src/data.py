import io
import math
from row import ROW
from cols import COLS
from utils import l_rnd

class DATA:
    ##fun unused so far
    def __new__(self, src, fun):
        self.rows = []
        self.cols = None
        if( type(src) is str):
            result = []
            with io.open(src, 'r') as file:
                for line in file:
                    row_values = line.strip().split(',')
                    self.add(self,row_values, fun)
            return
        else:
            for _, x in src.items() if src else {}:
                self.add(self, x, fun)

    def stats(self, cols, fun, ndivs, u):
        u = {".N": len(self.rows)}

        for col in (self.cols[cols] if cols else self.cols["y"]):
            stat_value = type(col).__dict__.get(fun, type(col).mid)(col)
            rounded_stat = l_rnd(stat_value, ndivs)
            u[col.txt] = rounded_stat

        return u
    


    def add(self, t, fun):
        if(hasattr(t, 'cells')):
            row = t.cells
        else:
            row = ROW(t)
        if(self.cols):
            if(fun):
                fun(self,row)
            else:
                self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)
        

    def mid(self, cols, u):
        u = []
        if (cols is not None):
            for col in cols:
                u.append(col.mid())
        else:
            for col in self.cols.all:
                u.append(col.mid())
        return ROW(u)

        
    
    def div(self, cols, u):
        u = []
        if (cols is not None):
            for col in cols:
                u.append(col.div())
        else:
            for col in self.cols.all:
                u.append(col.div())
        return ROW(u)
    
