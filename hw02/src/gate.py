from data import DATA
from test import Tests
import sys
# python3 gate.py -f ./data/auto93.csv -t stats > w2.out

class gate:
    def run(fileFlag, testFlag):
        if (testFlag== "stats"):
            Tests.stats(fileFlag)


for arg in sys.argv:
    print(arg)
