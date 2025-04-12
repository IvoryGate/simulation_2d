from src.tools.parse_flows_file import ParseFlows
from src.builder.generate_vehicles import GenerateVehicles

class LoadFlowsOnRoad:
    def __init__(
        self,
        start_time,
        end_time,
        flows_config_path,
        net
    ) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.flows_config_path =flows_config_path
        self.net = net

    @staticmethod
    def connect_road(net):
        for road in net.values():
            if road.leader_road_id != "null":
                print(road.leader_road_id)
                road.leader_road = net[road.leader_road_id]
            if road.follower_road_id != "null":
                road.follower_road_id = net[road.follower_road_id]
            if road.left_road_id != "null":
                road.left_road = net[road.left_road_id]
            if road.right_road_id != "null":
                road.right_road = net[road.right_road_id]


    def load_flows_cofig(self):
        flows_config = ParseFlows(self.flows_config_path).load_json()
        return flows_config

    def match_flows_and_roads(self):
        flows_dict = self.load_flows_cofig()
        combined_net_flows = {}
        for road in self.net:
            for key in flows_dict.keys():
                if road.id == key:
                    # print(road.central_line)
                    road.vehicles_list = GenerateVehicles(
                        start_time=self.start_time,
                        end_time=self.end_time,
                        max_interval=flows_dict[key]["max_interval"],
                        min_interval=flows_dict[key]["min_interval"],
                        flows=flows_dict[key]["flow"]
                    ).generate_vehicles(
                        current_pos_x=road.central_line,
                        current_pos_y=0,
                        current_velocity_x=0,
                        current_velocity_y=12,
                        current_acceleration_x=0,
                        current_acceleration_y=0,
                        next_pos_x=road.central_line,
                        next_pos_y=0,
                        next_velocity_x=0,
                        next_velocity_y=12,
                        next_acceleration_x=0,
                        next_acceleration_y=0,
                        on_which_road_id=key,
                        on_which_road=road,
                        leader=None,
                        follower=None
                    )
            combined_net_flows[f"{road.id}"] = road
        LoadFlowsOnRoad.connect_road(combined_net_flows)    
        return combined_net_flows
    
