from ..vehicle.base_vehicle import BaseVehicle

class Car(BaseVehicle):
    CAR_LENGTH:float = 5.0
    CAR_WIDTH:float = 2.0
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
        on_which_road: object, 
        leader: None, 
        follower: None, 
        depature_time: float, 
        car_length: float = CAR_LENGTH, 
        car_width: float = CAR_WIDTH
    ) -> None:
        super().__init__(
            current_pos_x, 
            current_pos_y, 
            current_velocity_x, 
            current_velocity_y, 
            current_acceleration_x, 
            current_acceleration_y,
            next_pos_x, 
            next_pos_y, 
            next_velocity_x, 
            next_velocity_y, 
            next_acceleration_x, 
            next_acceleration_y,
            on_which_road_id,
            on_which_road, 
            leader, 
            follower, 
            depature_time
        )
        self.car_length = car_length
        self.car_width = car_width
