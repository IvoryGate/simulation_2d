from src.road import Road
from vehicle.base_vehicle import BaseVehicle

class Car(BaseVehicle):
    def __init__(
        self, 
        id: str, 
        depature_time: float, 
        current_pos_x: float, 
        current_pos_y: float, 
        current_velocity_x: float, 
        current_velocity_y: float, current_acceleration_x: float, current_acceleration_y: float, 
        next_pos_x: float, 
        next_pos_y: float, 
        next_velocity_x: float, 
        next_velocity_y: float, 
        next_acceleration_x: float, next_acceleration_y: float, 
        on_which_road: Road
    ) -> None:
        super().__init__(id, depature_time, current_pos_x, current_pos_y, current_velocity_x, current_velocity_y, current_acceleration_x, current_acceleration_y, next_pos_x, next_pos_y, next_velocity_x, next_velocity_y, next_acceleration_x, next_acceleration_y, on_which_road)