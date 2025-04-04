from src.tools.parse_flows_file import ParseFlows

class LoadFlowsOnRoad():
    
    def load_flows_cofig(self):
        flows_config = ParseFlows(self.flows_config_path).load_json()
        return flows_config
    
    # def create_flows(self,net):
    #     flows_dict = self.load_net_config()
    #     flows = {}
    #     for key,value in flows_dict.items():
    #         vehicles = []
    #         for i in range(value):
    #             vehicles.append(
    #                 Car(
    #                     id = key,
                        
    #                 )
    #             )