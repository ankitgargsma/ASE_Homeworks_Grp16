from utils import *
from data import DATA
from num import NUM
from test import Tests
from sym import SYM
import sys
from collections import defaultdict

class gate:
    def run(self, fileFlag, testFlag):
        if testFlag == "stats":
            data = DATA(fileFlag)
            print(data.stats())
        elif testFlag == "csv_ascii":
            self.process_csv(fileFlag)
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
