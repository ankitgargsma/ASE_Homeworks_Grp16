from num import NUM
class Tests:
    def __init__(self):
        self.run_tests()
    
    def run_tests(self):
        self.test_num_initialization()
        self.test_num_add_method()
        self.test_num_mid_method()
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
Tests()