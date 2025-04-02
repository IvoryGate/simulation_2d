from src.road import Road

class BaseVehicle:
    DEPATURE_TIME: float = 0.0,
    def __init__(
        self,
        id: str,
        depature_time: float,
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
        on_which_road: Road,
    ) -> None:
        pass
    

