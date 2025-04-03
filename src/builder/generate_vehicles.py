import random
from ..vehicle.car import Car

class GenerateVehicles:
    FLOWS:int = 10

    def __init__(
        self,
        start_time:float,
        end_time:float,
        max_interval:float,
        min_interval:float,
        flows:int = FLOWS
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.max_interval = max_interval
        self.min_interval = min_interval
        self.flows = flows

    
    def calculate_total_time(self):
        return self.end_time - self.start_time

    
    def generate_per_vehicle_time(self):
        total_time = GenerateVehicles.calculate_total_time()
        time_series = [random.uniform(0, total_time) for _ in range(self.flows)]  # 随机生成车辆发车时间
        time_series.sort()                                                        # 排序，先保证是升序的
        for i in range(1, self.flows):                                            # 两辆车之间的时间间隔>=min_interval且<=max_interval
            interval = time_series[i] - time_series[i - 1] 
            if interval < self.min_interval:
                time_series[i] = time_series[i - 1] + self.min_interval
            elif interval > self.max_interval:
                time_series[i] = time_series[i - 1] + self.max_interval
        if time_series[-1] > total_time:
            time_series[-1] = total_time

        return time_series
    
    
    def generate_vehicles(
        self,
        id, 
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
        depature_time,
        car_length,
        car_width
    ) -> list:
        start_times = self.generate_per_vehicle_time()
        vehicles = []
        vehicles = [
            Car(
                id = id, 
                current_pos_x = current_pos_x, 
                current_pos_y = current_pos_y, 
                current_velocity_x = current_velocity_x, 
                current_velocity_y = current_velocity_y, 
                current_acceleration_x = current_acceleration_x, 
                current_acceleration_y = current_acceleration_y,
                next_pos_x = next_pos_x, 
                next_pos_y = next_pos_y, 
                next_velocity_x = next_velocity_x, 
                next_velocity_y = next_velocity_y, 
                next_acceleration_x = next_acceleration_x, 
                next_acceleration_y = next_acceleration_y,
                on_which_road_id = on_which_road_id,
                on_which_road = on_which_road, 
                leader = leader, 
                follower = follower, 
                depature_time = start_times[i],
                car_length = car_length,
                car_width = car_width
            )
            for i in range(self.flows)
        ]
        return vehicles