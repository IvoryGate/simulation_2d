import json

class ParseFlows():
    def __init__(
        self,
        flows_config_path,
    ) -> None:
        self.flows_config_path = flows_config_path

    def load_json(self):
        try:
            with open(self.flows_config_path,"r") as file:
                json_data = json.load(file)
        except FileNotFoundError:
            print(f"JSON file not found: {self.flows_config_path}")
        else:
            print(f"successfully load flows from {self.flows_config_path}")
            return json_data