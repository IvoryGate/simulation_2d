import unittest
import json

from src.tools.parse_config import ParseConfig
from src.tools.parse_net_file import ParseNet

class TestParse(unittest.TestCase):
    def test_load_json(self):
        config_path = "F:/桌面/simulation_2d/config.json"
        result = ParseConfig(config_path=config_path).load_json()
        print(type(result))
        print(result)

    def test_check_required_keys(self):
        config_path = "F:/桌面/simulation_2d/config.json"
        with open(config_path,"r") as file:
            json_data = json.load(file)
        data = json_data
        try:
            ParseConfig.check_essential_keys(data)
            print("All required keys are present.")
        except KeyError as e:
            print(f"Error: {e}")
    
    def test_load_net(self):
        net_config = "F:/桌面/simulation_2d/datas/net.json"
        result = ParseNet(net_config_path=net_config).load_json()
        print(type(result))
        print(result)