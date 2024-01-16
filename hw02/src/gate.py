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
            print(data.stats())
            Tests().run_tests()   

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
