import unittest
from src.builder.loop import Loop
from pympler import asizeof

class TestMain(unittest.TestCase):
    def test_memories(self):
        config_path = "F:/桌面/simulation_2d/config.json"
        main = Loop().run(config_path=config_path)
        memory_size = asizeof.asizeof(main)
        print(f"Total memory size of a: {memory_size} bytes")
