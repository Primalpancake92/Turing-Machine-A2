import unittest
from helper import TmSetup, ENTRY, random_input, random_arr
import random

"""
As gathered by the group chat, the outputs of the turing machine must be 
compared to the outputs of the turing machine from the tape to the expected 
output. 

The expected output relies on the built in sorting method of python, i.e.
python.sort(). Now we assert the output of the turing machine is the same as 
the output python.sort(). 

We will use this testing methodology for our valid, invalid, and edge test 
cases.
"""

class TestPositives(TmSetup):
    # Tests for sorted hex string values
    def test_asc_values(self):
        self.check_equality([
            ENTRY(f"{i}") for i in "0123456789ABCDEF"
        ])

    # Test for descending values
    def test_desc_values(self):
        self.check_equality([
            ENTRY(f"{i}") for i in "FEDCBA9876543210"
        ])
    
    # Testing realistic rng hex values
    def test_random_inputs(self):
        rng = random.Random(14)
        
        for i in range(2000):
            tape = [random_input(rng) for _ in range(rng.randint(2, 15))]
            with self.subTest(case=i, input=tape):
                self.check_equality(tape)
    
    # Testing realistic rng hex pairs only
    def test_random_pair(self):
        rng = random.Random(5)
        
        self.check_equality([random_input(rng), random_input(rng)])
    

if __name__ == "__main__":
    unittest.main(verbosity=2)