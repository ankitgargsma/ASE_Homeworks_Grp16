"""
(c) 2023, Tim Menzies, BSD-2

USAGE:
  python gate.py [OPTIONS]

OPTIONS:
  -c --cohen    small effect size               = .35
  -f --file     csv data file name              = ./data/diabetes.csv
  -h --help     show help                       = False
  -k --k        low class frequency kludge      = 1
  -m --m        low attribute frequency kludge  = 2
  -s --seed     random number seed              = 937162211
  -t --all      run all test-cases              = None
  -t --stats    print all stats                 = None

LIST OF TESTS:
  all test cases:
    'all'
"""
Seed = 937162211

help_str = __doc__

the = {
        'k': 1, 
        'm': 2
    }