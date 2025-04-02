import unittest

from unittest.mock import Mock
from src.road.base_road import BaseRoad
from src.vehicle.car import Car

class TestCar(unittest.TestCase):
    def test_car(self):
        road = BaseRoad('0',0.0,0.0,0.0,0.0,None)
        new_car = Car("0",0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,road,None,None,0.0,5.0,2.0)
        self.assertIsInstance(new_car,Car)

if __name__ == "__main__":
    unittest.main()