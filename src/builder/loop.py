from src.tools.parse_config import ParseConfig
from src.builder.build_net import BuildRoads
from src.builder.load_flows_on_road import LoadFlowsOnRoad
from src.tools.update import Update

class Loop:
    START_TIME:float = 0.0
    END_TIME:float = 3600.0
    PER_STEP:float = 0.1

    def __init__(
        self,
        start_time:float = START_TIME,
        end_time:float = END_TIME,
        per_step:float = PER_STEP 
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.per_step = per_step

    @staticmethod
    def float_range(start, stop, step):
        while start < stop:
            yield round(start,1)
            start += step

    def load_config(self,config_path) -> dict:
        config = ParseConfig(config_path=config_path).load_json()
        self.start_time = config["parameters"]["start_time"]
        self.end_time = config["parameters"]["end_time"]
        self.per_step = config["parameters"]["time_step"]
        self.net_config_path = config["paths"]["net_file"]
        self.flows_path = config["paths"]["flows_file"]

    def load_net(self):
        net = BuildRoads(self.net_config_path).build_net()
        return net
        
    def run(self,config_path):
        self.load_config(config_path=config_path)
        net = self.load_net()
        combined_net_flows = LoadFlowsOnRoad(
            start_time=self.start_time,
            end_time=self.end_time,
            flows_config_path=self.flows_path,
            net=net
        ).match_flows_and_roads()
        Update.init_sort_and_assign(combined_net_flows=combined_net_flows)
        update = Update(combined_net_flows=combined_net_flows)
        for step in Loop.float_range(self.start_time,self.end_time,self.per_step):
            update.get_step(step=step)
            update.update_all()