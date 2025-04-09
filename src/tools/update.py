from src.tools.state_controller import StateController
import numpy as np
import pandas as pd
import os
import threading
from multiprocessing import Pool

class Update:
    def __init__(
        self,
        delta_step,
        combined_net_flows,
        step = 0.0
    ) -> None:
        self.delta_step = delta_step
        self.combined_net_flows = combined_net_flows
        self.step = step

    @staticmethod
    def assign_leaders_and_followers(vehicles):
        if len(vehicles)!=0:
            vehicles[0].leader = None         # 第一辆车没有前车，最后一辆车没有后车
            vehicles[-1].follower = None
            for i in range(1, len(vehicles)):
                vehicles[i].leader = vehicles[i - 1]
                vehicles[i - 1].follower = vehicles[i]

    @staticmethod
    def init_sort_and_assign(combined_net_flows):
        for value in combined_net_flows.values():
            sorted_vehicle = sorted(value.vehicles_list, key=lambda vehicle: vehicle.depature_time)
            Update.assign_leaders_and_followers(vehicles = sorted_vehicle)
    
    @staticmethod
    def get_all_force(car):
        return StateController.handle_state(car=car)
    
    @staticmethod
    def get_speed(car):
        return np.sqrt(car.current_velocity_x**2 + car.current_velocity_y**2)

    def sort_and_assign(self):
        for value in self.combined_net_flows.values():
            sorted_vehicle = sorted(value.vehicles_list, key=lambda vehicle: vehicle.current_pos_y)
            Update.assign_leaders_and_followers(vehicles = sorted_vehicle)

    def get_step(self,step):
        self.step = step

    def get_next_acceleration(self,car):
        join_force = Update.get_all_force(car=car)
        car.next_acceleration_x = join_force[0][0]
        car.next_acceleration_y = join_force[1][0]

    def get_next_velocity(self,car):
        car.next_velocity_x = car.current_velocity_x + car.current_acceleration_x * self.delta_step 
        car.next_velocity_y = car.current_velocity_y + car.current_acceleration_y * self.delta_step 
        current_speed = Update.get_speed(car)        # 计算当前速度
        if current_speed > car.on_which_road.max_allowed_speed:       # 如果当前速度超过最大速度，则调整速度分量
            ratio = car.on_which_road.max_allowed_speed / current_speed     # 计算速度分量的比例因子
            car.next_velocity_x *= ratio
            car.next_velocity_y *= ratio

    def get_next_position(self,car):
        car.next_pos_x += car.current_velocity_x * self.delta_step + 0.5*car.current_acceleration_x*self.delta_step**2
        car.next_pos_y += car.current_velocity_y * self.delta_step + 0.5*car.current_acceleration_y*self.delta_step**2   

    def get_next_acceleration_velocity_position(self,car):
        self.get_all_force(car=car)
        self.get_next_velocity(car=car)
        self.get_next_position(car=car)

    def create_record_file(self,detail_output):
        column_structure = {
            "time": "float64",
            "id": "object",
            "a_x": "float64", 
            "a_y": "float64", 
            "v_x": "float64",
            "v_y": "float64", 
            "p_x": "float64", 
            "p_y": "float64",
            "road_id": "object"
        }
        df = pd.DataFrame(columns=column_structure.keys()).astype(column_structure)
        df.to_csv(
            detail_output,
            mode="a",
            header=not os.path.exists(detail_output),
            index=False
        )

    def check_chunk_size(self,df,filename):
        chunk_size = 1000
        if len(df) >= chunk_size:
            df.to_csv(
                filename,
                mode="a",
                header=not os.path.exists(filename),
                index=False
            )
            df = df.iloc[0:0]

    @staticmethod
    def unpdate_and_record_per_road(step,road_id,output_file):
        df = pd.DataFrame({})
        road = Update.combined_net_flows[f"{road_id}"]
        print("执行到这里了吗")
        for vehicle in road.vehicles_list:
            Update.get_next_acceleration_velocity_position(car=vehicle)
            vehicle.update_acceleration_velocity_position()
            new_df = pd.DataFrame({
                "time": step,
                "id": vehicle.id,
                "a_x": vehicle.current_acceleration_x, 
                "a_y": vehicle.current_acceleration_y, 
                "v_x": vehicle.current_velocity_x,
                "v_y": vehicle.current_velocity_y, 
                "p_x": vehicle.current_pos_x, 
                "p_y": vehicle.current_pos_y,
                "road_id": vehicle.on_which_road_id
            },index=[0])
            df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(
            output_file,
            mode="a",
            header=not os.path.exists(output_file),
            index=False
        )
        df = df.iloc[0:0]

    def print_test(self,num):
        print(f"{num}")

    def unpdate_and_record(self,output_file):
        pool = Pool(4)
        # iterator = [(road,output_file) for road in self.combined_net_flows.values()]
        step = self.step
        for road in self.combined_net_flows.values():
            road_id = road.id
            pool.apply_async(
                Update.unpdate_and_record_per_road,
                args=(step,road_id,output_file)
                )
        # for road in self.combined_net_flows.values():
        #     pool.apply_async(
        #         self.print_test,
        #         args=(self.step,)
        #         )
        pool.close()
        pool.join()
