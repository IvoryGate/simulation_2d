from src.road.base_road import BaseRoad
import uuid
class BaseVehicle:
    DEPATURE_TIME: float = 0.0,
    def __init__(
        self,
        current_pos_x: float,
        current_pos_y: float,
        current_velocity_x: float, 
        current_velocity_y: float,
        current_acceleration_x: float,
        current_acceleration_y: float,
        next_pos_x: float,
        next_pos_y: float,
        next_velocity_x: float, 
        next_velocity_y: float,
        next_acceleration_x: float,
        next_acceleration_y: float,
        on_which_road_id: str,
        on_which_road: BaseRoad,
        leader: None,
        follower: None,
        depature_time: float = DEPATURE_TIME,
    ) -> None:
        self.id = uuid.uuid4(), 
        self.depature_time = depature_time
        self.current_pos_x = current_pos_x
        self.current_pos_y = current_pos_y
        self.current_velocity_x = current_velocity_x 
        self.current_velocity_y = current_velocity_y
        self.current_acceleration_x = current_acceleration_x
        self.current_acceleration_y = current_acceleration_y
        self.next_pos_x = next_pos_x
        self.next_pos_y = next_pos_y
        self.next_velocity_x = next_velocity_x 
        self.next_velocity_y = next_velocity_y
        self.next_acceleration_x = next_acceleration_x
        self.next_acceleration_y = next_acceleration_y
        self.on_which_road_id = on_which_road_id
        self.on_which_road = on_which_road
        self.leader = leader
        self.follower = follower
    
    def update_acceleration_velocity_position(self):
        self.current_pos_x = self.next_pos_x
        self.current_pos_y = self.next_pos_y
        self.current_velocity_x = self.next_velocity_x
        self.current_velocity_y = self.next_velocity_y
        self.current_acceleration_x = self.next_acceleration_x
        self.current_acceleration_y = self.next_acceleration_y

    
