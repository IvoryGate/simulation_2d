import json

class ParseConfig():
    REQUIRED_KEYS = {
        "parameters": ["start_time", "end_time", "time_step"],
        "paths": ["net_file", "flows_file", "detail_output"],
        "functions": ["log"]
    }

    def __init__(
        self,
        config_path,
    ) -> None:
        self.config_path = config_path
        
    @staticmethod
    def check_essential_keys(json_data):
        for section, keys in ParseConfig.REQUIRED_KEYS.items():
            if section not in json_data:
                raise KeyError(f"Missing section: {section}")
            for key in keys:
                if key not in json_data[section]:
                    raise KeyError(f"Missing key: {key} in section {section}")
 
    def load_json(self):
        try:
            with open(self.config_path,"r") as file:
                json_data = json.load(file)
        except FileNotFoundError:
            print(f"JSON file not found: {self.config_path}")
        else:
            print(f"successfully load config from {self.config_path}")
            ParseConfig.check_essential_keys(json_data=json_data)
            return json_data

