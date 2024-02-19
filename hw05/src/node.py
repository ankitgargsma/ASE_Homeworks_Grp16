class NODE:
    def __init__(self, data):
        self.here = data
        self.lefts = None
        self.rights = None

    def walk(self, fun, depth=0):
        fun(self, depth, not (self.lefts or self.rights))
        if self.lefts:
            self.lefts.walk(fun, depth + 1)
        if self.rights:
            self.rights.walk(fun, depth + 1)

    def show(self, maxDepth=None):
        def d2h(data):
            return l_rnd(data.mid().d2h(self.here))
        
        maxDepth = 0
        def _show(node, depth, leafp):
            nonlocal maxDepth
            post = d2h(node.here) + "\t" + l.o(node.here.mid().cells) if leafp else ""
            maxDepth = max(maxDepth, depth)
            print(('|.. ' * depth) + post)
        
        self.walk(_show)
        print("")
        print(("    " * maxDepth) + str(d2h(self.here)) + l.o(self.here.mid().cells))
        print(("    " * maxDepth) + "_" + l.o(self.here.cols.names))