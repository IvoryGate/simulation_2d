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
        leader_road_id: str,
        follower_road_id: str,
        left_road_id: str,
        right_road_id: str,
        leader_road: object = None,
        follower_road: object = None,
        left_road: object = None,
        right_road: object = None,
        direction: list = DIRECTION

    ) -> None:
        self.id = id
        self.central_line = central_line
        self.road_length = road_length
        self.road_width = road_width
        self.max_allowed_speed = max_allowed_speed
        self.vehicles_list = vehicles_list
        self.leader_road_id = leader_road_id
        self.follower_road_id = follower_road_id
        self.left_road_id = left_road_id
        self.right_road_id = right_road_id
        self.leader_road = leader_road
        self.follower_road = follower_road
        self.left_road = left_road
        self.right_road = right_road
        self.direction = direction