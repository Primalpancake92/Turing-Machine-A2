import random 
import tm
import unittest

HEX = "0123456789ABCDEF"
ENTRY = lambda h: h*16


def random_input(rng, digits=HEX):
    return "".join(rng.choice(digits) for _ in range(16))


def random_arr(rng, max=10, digits=HEX):
    return [random_input(rng, digits) for _ in range(rng.randint(0, max))]


class TmSetup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.machine, _ = tm.load("TurningMachine.tsv")
    
    
    def check_equality(self, input):
        tape = "[" + ",".join(input) + "]"
        expected = "[" + ",".join(sorted(input)) + "]"
        
        c = tm.run(self.machine, tape, max_steps=1000000)
        
        # Must assert the TM will produce the same output as the built in sort()
        self.assertEqual(c.state, tm.ACCEPT)
        #the head must be at 0 after its number of input are exhausted and rewind.
        self.assertEqual(c.head, 0)
        # assert the returned tape is equal to the expected tape.
        self.assertEqual(tm.tape_string(c), expected)