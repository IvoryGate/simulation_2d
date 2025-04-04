import unittest
from src.builder.loop import Loop

class TestLoop(unittest.TestCase):
    def test_float_range(self):
        result = list(Loop.float_range(0.0,20.0,0.1))
        expect_result = [round(n*0.1,1) for n in range(200)]
        self.assertEqual(result,expect_result)

