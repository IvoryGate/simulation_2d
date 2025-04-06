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

    def load_flows_cofig(self):
        flows_config = ParseFlows(self.flows_config_path).load_json()
        return flows_config

    def match_flows_and_roads(self):
        flows_dict = self.load_flows_cofig()
        combined_net_flows = {}
        for road in self.net:
            for key in flows_dict.keys():
                if road.id == key:
                    road.vehicles_list = GenerateVehicles(
                        start_time=self.start_time,
                        end_time=self.end_time,
                        max_interval=flows_dict[key]["max_interval"],
                        min_interval=flows_dict[key]["min_interval"],
                        flows=flows_dict[key]["flow"]
                    ).generate_vehicles(
                        id=key,
                        current_pos_x=road.central_line,
                        current_pos_y=0,
                        current_velocity_y=road.max_allowed_speed,
                        current_velocity_x=0,
                        current_acceleration_x=0,
                        current_acceleration_y=0,
                        next_pos_x=None,
                        next_pos_y=None,
                        next_velocity_x=None,
                        next_velocity_y=None,
                        next_acceleration_x=None,
                        next_acceleration_y=None,
                        on_which_road_id=key,
                        on_which_road=road,
                        leader=None,
                        follower=None
                    )
            combined_net_flows[f"{road.id}"] = road
        return combined_net_flows