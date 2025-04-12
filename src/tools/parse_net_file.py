import json
class ParseNet:

    def __init__(
        self,
        net_config_path,
    ) -> None:
        self.net_config_path = net_config_path

    def load_json(self):
        try:
            with open(self.net_config_path,"r") as file:
                json_data = json.load(file)
        except FileNotFoundError:
            print(f"JSON file not found: {self.net_config_path}")
        else:
            print(f"successfully load net from {self.net_config_path}")
            return json_data