from utils import *
from data import DATA
from num import NUM
from test import Tests
from sym import SYM
import sys
from config import *
from range import Range
from range import *
from collections import defaultdict
from rule import RULE
from rules import RULES

class gate:
    def run(self, fileFlag, testFlag):
        t = settings(help_str)

        if testFlag == "stats":
            data = DATA(fileFlag)
            print(data.stats())
        elif testFlag == "csv_ascii":
            self.process_csv(fileFlag)
        elif testFlag == "all":
            Tests().run_tests()
        elif testFlag == "bayes":
            self.bayes();
        elif testFlag == "km_feature":
            self.km_func();
        elif testFlag == "gateFor20":
            self.run_specific_test(testFlag)
        elif testFlag == "gate":
            self.run_specific_test(testFlag)
        elif testFlag == "bins":
            self.bins()
        else:
            self.run_specific_test(testFlag)  

    def run_specific_test(self, test_name):
        test_method = getattr(Tests(), f'{test_name}', None)
        if test_method:
            test_method()
            print("PASS")
        else:
            print(f"Unknown test: {test_name}")

    def learn(self, data, row, my):
            my['n'] += 1
            kl = row.cells[data.cols.klass.at]
            if my['n'] > 10:
                my['tries'] += 1
                my['acc'] += 1 if kl == row.likes(my['datas'])[0] else 0
            my['datas'][kl] = my['datas'].get(kl, DATA(data.cols.names))
            my['datas'][kl].add(row)

    def bayes(self):
            wme = {'acc': 0, 'datas': {}, 'tries': 0, 'n': 0}
            DATA(t['file'], lambda data, t: self.learn(data, t, wme))
            accuracy = (wme['acc'] / wme['tries'])*100
            print(accuracy)
    
    def km_func(self):
            highest_k, highest_m = None, None
            highest_accuracy = 0
            for k in range(4):
                for m in range(1, 4):
                    the['k'] = k
                    the['m'] = m
                    wme = {"acc": 0, "datas": {}, "tries": 0, "n": 0}
                    DATA(t['file'], lambda data, t: self.learn(data, t, wme))
                    accuracy = (wme['acc'] / wme['tries']) * 100
                    print(f'For k value = {k} and m value = {m}, accuracy is {accuracy:.2f}%')
                    if accuracy > highest_accuracy:
                        highest_accuracy = accuracy
                        highest_k, highest_m = k, m

            print(f'Recommended combination is: k value = {highest_k}, m value = {highest_m}, with the best accuracy of {highest_accuracy:.2f}%')

    def process_csv(self, file_path):
        class_counts = defaultdict(int)
        total_rows = 0

        try:
            for line_num, data_row in csv(file_path):
                class_label = data_row[-1] 
                if class_label.lower() == "class!":
                    continue
                total_rows += 1
                class_counts[class_label] += 1

        except FileNotFoundError as e:
            print(f"Error: {e}")

        # Print the results in an ASCII table
        print("Class | Count | Percentage")
        print("-" * 29)

        for class_label, count in class_counts.items():
            percentage = (count / total_rows) * 100
            print(f"{class_label.ljust(6)}| {str(count).rjust(5)} | {percentage:.2f}%")

        print("-" * 29)
        print(f"Total | {total_rows} | 100.00%")

    def bins(self):
        d = DATA("./auto93.csv")
        best, rest, _ = d.branch()
        #LIKE = list(best.rows.values())
        LIKE = best.rows
        HATE = random.sample(rest.rows, min(3 * len(LIKE), len(rest.rows)))

        def score(range_):
            return range_.score("LIKE", len(LIKE), len(HATE))

        t = []
        #for col in list(d.cols.x.values()):
        for col in list(d.cols.x):
            print("")
            for range_ in ranges1(col, {"LIKE": LIKE, "HATE": HATE}):
                print(range_)
                t.append(range_)

        '''t.sort(key=lambda a: score(a), reverse=True)
        max_score = score(t[0])
        print("\n#scores:\n")
        #for v in t[:Constants.the.Beam]:
        for v in t[:THE_BEAM]:
            if score(v) > max_score * 0.1:
                 print("{:.2f}".format(round(score(v), 2)), v)
        
        print({"LIKE": len(LIKE), "HATE": len(HATE)})
    
        '''

def _ranges(cols, rowss):
    t = []
    for col in cols:
        for range in ranges1(col, rowss):
            t.append(range)
    return t

def o(t, n=None, u=None):
    if isinstance(t, (int, float)):
        return str(round(t, n))
    if not isinstance(t, dict):
        return str(t)

    u = []
    for k, v in t.items():
        if str(k)[0] != "_":
            if len(t) > 0:
                u.append(o(v, n))
            else:
                u.append(f"%s: %s", o(k, n), o(v, n))

    return "{" + ", ".join(u) + "}"

def shuffle(t):
    u = t.copy()
    for i in range(len(u) - 1, 0, -1):
        j = random.randint(0, i)
        u[i], u[j] = u[j], u[i]
    return u

if __name__ == "__main__":
    t = settings(help_str)
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

    
    ##final hw
    print("score    mid selected                                          rule")
    print("-----   --------------------------------------------------     ------")

    d = DATA("./auto93.csv")
    tmp = shuffle(d.rows)
    train = d.clone(tmp[:len(tmp) // 2])
    test = d.clone(tmp[len(tmp) // 2:])
    test.rows.sort(key=lambda row: row.d2h(d))
    test.rows = shuffle(test.rows)
    best0, rest, evals1 = train.branch(THE_CUT1)
    best, _, evals2 = best0.branch(THE_CUT2)
    LIKE = best.rows
    HATE = slice(shuffle(rest.rows), 1, 3 * len(LIKE))
    rowss = {'LIKE': LIKE, 'HATE': HATE}
    test.rows = shuffle(test.rows)
    random = test.clone(slice(test.rows, 1, int(evals1 + evals2 + THE_CUT2 - 1)))
    random.rows.sort(key=lambda row: row.d2h(d))
    for i, rule in enumerate(RULES(_ranges(train.cols.x, rowss), "LIKE", rowss).sorted):
        result = train.clone(rule.selects(test.rows))
        if len(result.rows) > 0:
            result.rows.sort(key=lambda row: row.d2h(d))
            print(round(rule.scored), "\t", o(result.mid().cells), "\t", rule.show())