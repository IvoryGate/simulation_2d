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
                id=key,
                central_line=value["central_line"],
                road_length=value["road_length"],
                road_width=value["road_width"],
                max_allowed_speed=value["max_allowed_speed"],
                vehicles_list=[],
                leader_road_id = value["leader_road_id"],
                follower_road_id = value["follower_road_id"],
                left_road_id = value["left_road_id"],
                right_road_id = value["right_road_id"],
                direction=value["direction"]
            )
            net.append(road)
        return net
