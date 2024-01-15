from io import StringIO
from num import NUM
from sym import SYM
from data import DATA
from utils import *
import math
class Tests:
    
    def run_tests(self):
        self.test_num_initialization()
        self.test_num_add_method()
        self.test_num_mid_method()
        self.test_num_div_method()
        self.test_num_norm_method()
        self.test_sym()
        self.test_data_initialization_from_file()
        self.test_data_initialization_from_dict()
        self.stats()
        print("PASS")

    ## Helper function
    def assert_equal(self, actual, expected):
        assert actual == expected, f"Expected {expected}, but got {actual}"

    def test_num_initialization(self):
        self.num_instance = NUM("a", 5)
        self.assert_equal(self.num_instance.s, "a")
        self.assert_equal(self.num_instance.at, 5)
        self.assert_equal(self.num_instance.n, 0)
        self.assert_equal(self.num_instance.mu, 0)
        self.assert_equal(self.num_instance.m2, 0)
        self.assert_equal(self.num_instance.hi, float('-inf'))
        self.assert_equal(self.num_instance.lo, float('inf'))
        self.assert_equal(self.num_instance.heaven, 1)

    def test_num_add_method(self):
        self.num_instance = NUM("a", 5)
        self.num_instance.add(10, 2)
        self.assert_equal(self.num_instance.n, 1)
        self.assert_equal(self.num_instance.mu, 10)
        self.assert_equal(self.num_instance.m2, 0)
        self.assert_equal(self.num_instance.lo, 10)
        self.assert_equal(self.num_instance.hi, 10)

        self.num_instance.add(20, 3)
        self.assert_equal(self.num_instance.n, 2)
        self.assert_equal(self.num_instance.mu, 15)
        self.assert_equal(self.num_instance.m2, 50)
        self.assert_equal(self.num_instance.lo, 10)
        self.assert_equal(self.num_instance.hi, 20)

    def test_num_mid_method(self):
        self.num_instance = NUM("a", 5)
        self.num_instance.add(10, 2)
        self.num_instance.add(20, 3)
        self.num_instance.add(30, 4)
        self.num_instance.add(40, 5)
        self.num_instance.add(50, 6)
        self.assert_equal(self.num_instance.mid(), 30)
    
    def test_num_div_method(self):
        self.num_instance = NUM("a", 5)
        self.num_instance.add(10, 2)
        self.num_instance.add(20, 3)
        self.assert_equal(round(self.num_instance.div(), 3), 7.071)

    def test_num_norm_method(self):
        num_instance = NUM("a", 5)
        self.assert_equal(num_instance.norm("?"), "?")

        num_instance.add(10, 2)
        num_instance.add(20, 3)
        self.assert_equal(round(num_instance.norm(10), 3), 0)

    def test_sym(self):
        sym = SYM()
        for x in ["a","a","a","a","b","b","c"]:
            sym.add(x)
        return "a" == sym.mid() and 1.379 == rnd(sym.div())
    
    def test_data_initialization_from_file(self):
        self.saved_stdout = sys.stdout
        sys.stdout = StringIO()
        data_instance = DATA("./data/auto93.csv", None)
        self.assertEqual(len(data_instance.rows), 399)
    
    def test_data_initialization_from_dict(self):
        data_dict = {
            "row1": [1, 2, 3],
            "row2": [4, 5, 6],
        }
        data_instance = DATA(data_dict, None)
        self.assertEqual(len(data_instance.rows), len(data_dict))

    def stats(self, file):
        self.saved_stdout = sys.stdout
        sys.stdout = StringIO()
        data_instance = DATA(file, None)
        cols = None
        ndivs = 2
        u = {}

        result = data_instance.stats(cols, None, ndivs, u)
        print(result)
        self.assertEqual(result[".N"], len(data_instance.rows))
