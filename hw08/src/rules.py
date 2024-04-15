from rule import RULE
from utils import *

class RULES:
    def __init__(self, ranges, goal, rowss):
        for k, v in rowss.items():
            print(k, len(v))

        self.goal = goal
        self.rowss = rowss
        self.LIKE = 0
        self.HATE = 0
        self.likeHate()

        self.sorted = self.top(self.tryy(self.top(ranges)))

    def likeHate(self):
        for y, rows in self.rowss.items():
            if y == self.goal:
                self.LIKE += len(rows)
            else:
                self.HATE += len(rows)

    def score(self, t):
        like, hate, tiny = 0, 0, 1E-30
        for klass, n in t.items():
            if klass == self.goal:
                like += n
            else:
                hate += n
        like, hate = like/(self.LIKE + tiny), hate/(self.HATE + tiny)
        if hate > like:
            return 0
        else:
            return (like**THE_SUPPORT)/(like + hate)

    def tryy(self, ranges):
        u = []
        for subset in powerset(ranges):
            if len(subset) > 0:
                rule = RULE(subset)
                rule.scored = self.score(rule.selectss(self.rowss))
                if rule.scored > 0.01:
                    u.append(rule)
        return u

    def top(self, t):
        t.sort(key=lambda x: x.scored, reverse=True)
        u = []
        for x in t:
            if x.scored > t[0].scored * THE_CUT:
                u.append(x)
        return u[:THE_BEAM]