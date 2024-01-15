from data import DATA
from test import Tests
import sys
# python gate.py -f ./data/auto93.csv -t stats > w2.out

class gate:
    def run(fileFlag, testFlag):
        if (testFlag== "stats"):
            test = Tests()
            test.stats(fileFlag)


i= 0
for arg in sys.argv:
    if(arg == "-f"):
        fileFlag = sys.argv[i+1]
    if(arg == "-t"):
        testFlag = sys.argv[i+1]
    i = i+ 1
gate.run(fileFlag, testFlag)
