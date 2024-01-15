from data import DATA
from test import stats
# python3 gate.py -f hw02/src/data/auto93.csv -t stats > w2.out

class gate:
    def run(fileFlag, testFlag):
        if (testFlag== "stats"):
            stats(fileFlag)


