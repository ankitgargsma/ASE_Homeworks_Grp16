from utils import *
from data import DATA
from num import NUM
from test import Tests
from sym import SYM
import sys

class gate:
    def run(self, fileFlag, testFlag):
        if testFlag == "stats":
            data = DATA(fileFlag)
            self.stats(data)
        elif testFlag == "all":
            Tests().run_tests()
        else:
            self.run_specific_test(testFlag)

    def stats(self, data):
        for col in data.cols.all:
            if isinstance(col, NUM):
                mean = col.mid()
                print(f"Mean for numerical class '{col.txt}': {mean}")
            elif isinstance(col, SYM):
                mode = col.mid()
                print(f"Mode for symbolic class '{col.txt}': {mode}")

    def run_specific_test(self, test_name):
        test_method = getattr(Tests(), f'{test_name}', None)
        if test_method:
            test_method()
            print("PASS")
        else:
            print(f"Unknown test: {test_name}")

if __name__ == "__main__":
    fileFlag, testFlag = None, None

    i = 0
    for arg in sys.argv:
        if arg == "-f":
            fileFlag = sys.argv[i + 1]
          
        if arg == "-t":
            testFlag = sys.argv[i + 1]
        
        i = i + 1

    if fileFlag and testFlag:
        g = gate()
        g.run(fileFlag, testFlag)
