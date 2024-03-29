from row import ROW
from cols import COLS
from sym import SYM
from num import NUM
from utils import *;
import random
import config
import utils

class DATA:

    #Global declaration . Although not preferred. Need to fix later
    list_1, list_2, list_3, list_4, list_5, list_6 = [[] for _ in range(6)]

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
        u = []
        for col in cols or self.cols.all:
            u.append(col.mid())
        return ROW(u)
    
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

    def split(self, best, rest, lite, dark):
        selected = DATA(self.cols.names)
        max = 1e30
        out = 1

        for i, row in enumerate(dark):
            b = row.like(best, len(lite), 2)
            r = row.like(rest, len(lite), 2)
            if b > r:
                selected.add(row)

            tmp = abs(b + r) / abs(b - r + 1e-300)
            if tmp > max:
                out, max = i, tmp
        return out, selected

    
    def best_rest(self, rows, want, best=None, rest=None):
        rows.sort(key=lambda x: x.d2h(self))
        best, rest = DATA(self.cols.names), DATA(self.cols.names)
        for i in range(len(rows)):
            if i <= want:
                best.add(rows[i])
            else:
                rest.add(rows[i])
        return best, rest
    
    def gate(self, budget0, budget, some):
        random.seed(set_random_seed())
        rows = random.sample(self.rows, len(self.rows)) 
        #y values of first 6 examples in ROWS
        DATA.list_1.append(f"1. top6: {[r.cells[len(r.cells)-3:] for r in rows[:6]]}")
        
        # y values of first 50 examples in ROWS
        DATA.list_2.append(f"2. top50:{[[r.cells[len(r.cells)-3:] for r in rows[:50]]]}")
        
        rows.sort(key=lambda row: row.d2h(self))
        # y values of ROW[1]
        DATA.list_3.append(f"3. most: {rows[0].cells[len(rows[0].cells)-3:]}")

        random.shuffle(rows)
        lite = rows[:budget0]
        dark = rows[budget0:]
        bests = []
        stats = []

        for i in range(budget):
            best, rest = self.best_rest(lite, (len(lite) ** some))
            todo, selected = self.split(best, rest, lite, dark)
            # y values of centroid of (from DARK, select BUDGET0+i rows at random)
            selected_rows_rand = random.sample(dark, budget0+i)
            y_values_sum = [0.0, 0.0, 0.0]
            for row in selected_rows_rand:
                y_val = list(map(coerce, row.cells[-3:]))
                y_values_sum = [sum(x) for x in zip(y_values_sum, y_val)]
            num_rows = len(selected_rows_rand)
            y_values_centroid = [round(val / num_rows,2) for val in y_values_sum]

            DATA.list_4.append(f"4: rand:{y_values_centroid}")
            # y values of centroid of SELECTED
            DATA.list_5.append(f"5. mid: {selected.mid().cells[len(selected.mid().cells)-3:]}")
            # y values of first row in BEST
            DATA.list_6.append(f"6. top: {best.rows[0].cells[len(best.rows[0].cells)-3:]}")

            stats.append(selected.mid())
            bests.append(best.rows[0])
            lite.append(dark.pop(todo))
            
        return stats, bests
    
    def farApart(self, rows, sortp=True, a=None):
        far = int((len(rows) * utils.THE_FAR) // 1)
        evals = 1 if a else 2
        a = a or any(rows).neighbors(self, rows)[far]
        b = a.neighbors(self, rows)[far]
        if sortp and b.d2h(self) < a.d2h(self):
            a, b = b, a
        return a, b, a.dist(b, self), evals
    
    def stats(self, cols=None, callback=None, ndivs=None, u=None):
        u = {}
        for _, col in (cols or self.cols.x).items():
            u[col.txt] = round(type(col).__getattribute__(col, callback or "mid")(), ndivs)
        for _, col in (cols or self.cols.y).items():
            u[col.txt] = round(type(col).__getattribute__(col, callback or "mid")(), ndivs)
        return list(u.values())

    def stats_divs(self, cols=None, callback=None, ndivs=None, u=None):
        u = {}
        for _, col in (cols or self.cols.x).items():
            u[col.txt] = round(type(col).__getattribute__(col, callback or "div")(), ndivs)
        for _, col in (cols or self.cols.y).items():
            u[col.txt] = round(type(col).__getattribute__(col, callback or "div")(), ndivs)
        return list(u.values())

    def randN(self, n=0):
        rows = list(self.rows.values())
        random.shuffle(rows)
        rowsN = rows[:n]
        rowsNd2h = [row.d2h(self) for row in rowsN]
        rowsNd2h.sort()
        s_temp = ""

        for j in rowsNd2h:
            s_temp += str(round(j,2))
            s_temp += "\t"
        print("N: ",n)
        print("randN:\t",s_temp)