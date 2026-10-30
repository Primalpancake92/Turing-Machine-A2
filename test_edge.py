import unittest
from helper import TmSetup, ENTRY, random_input, random_arr
import random


class TestEdgeCases(TmSetup):
    # Tests the empty tapes.
    def test_empty_arr(self):
        self.check_equality([])
    
    # Tests already sorted tapes.
    def test_already_sorted(self):
        rng = random.Random(32)
        
        test_values = [random_input(rng) for _ in range(10)];
                
        self.check_equality(sorted(test_values))
        
    # Testing a tape of equal entries
    def test_equal(self):
        self.check_equality([ENTRY("A") for _ in range(5)])
        
    
    # Tests for a single entry on the tape
    def test_single(self):
        rng = random.Random(19)
        
        self.check_equality([random_input(rng)])
        
        
if __name__ == "__main__":
    unittest.main(verbosity=2)