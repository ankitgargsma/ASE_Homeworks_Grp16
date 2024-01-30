from io import StringIO
from num import NUM
from sym import SYM
from cols import COLS
from data import DATA
from utils import *
import math
import sys 
import platform
import os 
from config import *
import random

class MockRow:
    def __init__(self, cells):
        self.cells = cells

class Tests:
    
    def run_tests(self):
        self.test_num_initialization()
        self.test_num_add_method()
        self.test_num_mid_method()
        self.test_num_div_method()
        self.test_num_norm_method()
        self.test_sym()
        #self.test_data_initialization_from_file()
        #self.test_data_initialization_from_dict()
        #self.stats()
        self.test_div_with_different_data()
        self.test_add()
        self.test_mid()
        self.test_div()
        self.test_Util_cells()
        self.test_coerce()
        self.test_roundNumbers()
        self.testAddInSym()
        self.coerceTest2()
        self.UtilsAnswerCheck()
        self.random_cells_test()
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
        self.num_instance.add(10)
        self.assert_equal(self.num_instance.n, 1)
        self.assert_equal(self.num_instance.mu, 10)
        self.assert_equal(self.num_instance.m2, 0)
        self.assert_equal(self.num_instance.lo, 10)
        self.assert_equal(self.num_instance.hi, 10)

        self.num_instance.add(20)
        self.assert_equal(self.num_instance.n, 2)
        self.assert_equal(self.num_instance.mu, 15)
        self.assert_equal(self.num_instance.m2, 50)
        self.assert_equal(self.num_instance.lo, 10)
        self.assert_equal(self.num_instance.hi, 20)

    def test_num_mid_method(self):
        self.num_instance = NUM("a", 5)
        self.num_instance.add(10)
        self.num_instance.add(20)
        self.num_instance.add(30)
        self.num_instance.add(40)
        self.num_instance.add(50)
        self.assert_equal(self.num_instance.mid(), 30)
    
    def test_num_div_method(self):
        self.num_instance = NUM("a", 5)
        self.num_instance.add(10)
        self.num_instance.add(20)
        self.assert_equal(round(self.num_instance.div(), 3), 7.071)

    def test_num_norm_method(self):
        num_instance = NUM("a", 5)
        self.assert_equal(num_instance.norm("?"), "?")

        num_instance.add(10)
        num_instance.add(20)
        self.assert_equal(round(num_instance.norm(10), 3), 0)

    def test_sym(self):
        sym = SYM()
        for x in ["a","a","a","a","b","b","c"]:
            sym.add(x)
        return "a" == sym.mid() and 1.379 == rnd(sym.div())
    
    def test_add(self):
        sym_obj = SYM()
        sym_obj.add("basketball")
        assert sym_obj.n == 1
        assert sym_obj.has == {"basketball": 1}
        assert sym_obj.mode == "basketball"
        assert sym_obj.most == 1

        sym_obj.add("football")
        sym_obj.add("basketball")
        assert sym_obj.n == 3
        assert sym_obj.has == {"basketball": 2, "football": 1}
        assert sym_obj.mode == "basketball"
        assert sym_obj.most == 2

    def test_mid(self):
        sym_obj = SYM()
        sym_obj.add("baseball")
        sym_obj.add("basketball")
        assert sym_obj.mid() == "baseball"

    def test_div(self):
        sym_obj = SYM()
        sym_obj.add("footall")
        sym_obj.add("baseball")
        sym_obj.add("Formula1")
        sym_obj.add("basketball")
        assert math.isclose(sym_obj.div(), 2.0)

    def test_div_with_different_data(self):
        # Test the div method with a different dataset
        data = ["x", "x", "y", "y", "z"]
        sym = SYM()
        for x in data:
            sym.add(x)

        expected_result = -((2/5) * math.log2(2/5) + (2/5) * math.log2(2/5) + (1/5) * math.log2(1/5))

    def test_data_initialization_from_file(self):
        self.saved_stdout = sys.stdout
        sys.stdout = StringIO()
        data_instance = DATA("./auto93.csv", None)
        self.assert_equal(len(data_instance.rows), 398)
    
    def test_Util_cells(self):
        input_str = "1, 2, 123789, true, false, null, AA24"
        result = cells(input_str)
        assert result == [1, 2, 123789, 'true', 'false', 'null', "AA24"]

    def test_coerce(self):
        values_to_test = [("100", 100), ("3.14", 3.14), 
                          ("False", False), ("Hello", "Hello")]
        for input_val, expected_output in values_to_test:
            assert coerce(input_val) == expected_output

    def test_roundNumbers(self):
        numbers_to_round = [(3.14159, 2, 3.14), (10.8, 0, 11), 
                        (0.333, 1, 0.3)]
        for num, precision, expected in numbers_to_round:
            assert round(num, precision) == expected

    def testAddMid(self):
        num_object = NUM('','')
        for num in [200, 300, 400, 500, 600]:
            num_object.add(num)
        assert num_object.mid() == 400
    
    def testAddInSym(self):
        sym_obj = SYM()
        for x in ["c","c","c","b","b","c","d"]:
            sym_obj.add(x)
        return sym_obj.mid() == "c"

    def coerceTest2(self):
        dict_ex = coerce("{'a': 1, 'b': 2}")
        return type(dict_ex) == dict
    
    def UtilsAnswerCheck(self):
        out = output({"a": 1, "b": 2})
        return out == "{a: 1, b: 2}"
    
    def reset_seed(self):
        random.seed(Seed)

    def gateFor20(self):
       self.reset_seed()
       print("#best, mid")
       for i in range(20):
           d = DATA("./auto93.csv")
           stats, bests = d.gate(4, 16, 0.5)
           stat, best = stats[-1], bests[-1]
           print(round(best.d2h(d), 2), round(stat.d2h(d), 2))



    '''def test_data_initialization_from_dict(self):
        data_dict = {
            "row1": [1, 2, 3],
            "row2": [4, 5, 6],
        }
        data_instance = DATA(data_dict, None)
        self.assertEqual(len(data_instance.rows), len(data_dict))
    '''

    '''def stats(self, file):
        self.saved_stdout = sys.stdout
        sys.stdout = StringIO()
        data_instance = DATA(file, None)
        cols = None
        ndivs = 2
        u = {}

        result = data_instance.stats(cols, None, ndivs, u)
        print(result)
        self.assertEqual(result[".N"], len(data_instance.rows))
    
'''

    def random_cells_test(self):
        random_numbers = [random.randint(1, 100) for _ in range(5)]
        input_str = ", ".join(map(str, random_numbers))
        result = cells(input_str)
        assert result == random_numbers
#test_instance = Tests()
#test_instance.run_tests()