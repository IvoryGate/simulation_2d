import unittest
from unittest.mock import Mock

from ..src.vehicle.car import Car
class TestCar(unittest.TestCase):
    def test_car():
        mock = Mock()
        mock.getRoad.return_value = "abv"
        print(mock.getRoad())

