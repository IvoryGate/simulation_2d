from src.tools.parse_config import ParseConfig
from src.builder.build_net import BuildRoads

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

    def load_net(self):
        net = BuildRoads(self.net_config_path).build_net()
        return net
        

    def run(self,config_path):
        self.load_config(config_path=config_path)
        net = self.load_net()
        print(net)
        # for step in Loop.float_range(self.start_time,self.end_time,self.per_step):
        #     print(step)
