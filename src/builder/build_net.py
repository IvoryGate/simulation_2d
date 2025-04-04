from src.tools.parse_net_file import ParseNet
from src.road.base_road import BaseRoad
class BuildRoads:
    def __init__(
        self,
        net_config_path
    ):
        self.net_config_path = net_config_path

    def load_net_cofig(self):
        net_config = ParseNet(self.net_config_path).load_json()
        return net_config
    
    def build_net(self):
        net = []
        net_dict = self.load_net_cofig()
        for key,value in net_dict.items():
            road = BaseRoad(
                key,
                value["central_line"],
                value["road_length"],
                value["road_width"],
                value["max_allowed_speed"],
                [],
                value["direction"]
            )
            net.append(road)
        return net