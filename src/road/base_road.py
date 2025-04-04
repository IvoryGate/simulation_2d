"""
This class `BaseRoad` is 
"""
class BaseRoad:
    DIRECTION = (0.0,1.0)
    def __init__(
        self,
        id: str,
        central_line: float,
        road_length: float,
        road_width: float,
        max_allowed_speed: float,
        vehicles_list: list,
        direction: list = DIRECTION
    ) -> None:
        self.id = id
        self.central_line = central_line
        self.road_length = road_length
        self.road_width = road_width
        self.max_allowed_speed = max_allowed_speed
        self.vehicles_list = vehicles_list
        self.direction = direction
    
