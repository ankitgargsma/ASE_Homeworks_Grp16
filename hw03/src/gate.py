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
        elif testFlag == "all":
            Tests().run_tests()
        else:
            self.run_specific_test(testFlag)  

    def run_specific_test(self, test_name):
        test_method = getattr(Tests(), f'{test_name}', None)
        if test_method:
            test_method()
            print("PASS")
        else:
            print(f"Unknown test: {test_name}")

    def learn(data, row, my, n_hypotheses, most, tmp, out):
            my['n'] += 1
            kl = row.cells[data.cols.klass.at]
            if my['n'] > 10:
                my['tries'] += 1
                my['acc'] += 1 if kl == row.likes(my['datas'], my['n'], n_hypotheses, most, tmp, out)[0] else 0
            my['datas'][kl] = my['datas'].get(kl, DATA(data.cols.names))
            my['datas'][kl].add(row)

    def bayes():
            wme = {'acc': 0, 'datas': {}, 'tries': 0, 'n': 0}
            n_hypotheses, most, tmp, out = 0, None, None, None 
            DATA(t['file'], lambda data, t: learn(data, t, wme, n_hypotheses, most, tmp, out))
            accuracy = wme['acc'] / wme['tries']
            print(accuracy)
            return accuracy

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
