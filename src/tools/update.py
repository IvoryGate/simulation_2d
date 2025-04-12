from src.tools.state_controller import StateController
import numpy as np
import pandas as pd
import os
import pickle
from multiprocessing import Pool
import multiprocessing
import time
import sys

class Update:
    COMBINED_NET_FLOWS = {}
    def __init__(
        self,
        delta_step,
        combined_net_flows,
        step = 0.0
    ) -> None:
        self.delta_step = delta_step
        self.combined_net_flows = combined_net_flows
        self.step = step
        Update.COMBINED_NET_FLOWS = combined_net_flows


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

    @staticmethod
    def get_next_acceleration(car):
        join_force = Update.get_all_force(car=car)
        car.next_acceleration_x = join_force[0][0]
        car.next_acceleration_y = join_force[1][0]

    @staticmethod
    def get_next_velocity(car):
        car.next_velocity_x = car.current_velocity_x + car.next_acceleration_x * 0.1 
        car.next_velocity_y = car.current_velocity_y + car.next_acceleration_y * 0.1
        current_speed = Update.get_speed(car)        # 计算当前速度
        if current_speed > car.on_which_road.max_allowed_speed:       # 如果当前速度超过最大速度，则调整速度分量
            ratio = car.on_which_road.max_allowed_speed / current_speed     # 计算速度分量的比例因子
            car.next_velocity_x *= ratio
            car.next_velocity_y *= ratio

    @staticmethod
    def get_next_position(car):
        car.next_pos_x += car.next_velocity_x * 0.1 + 0.5*car.next_acceleration_x*0.1**2
        car.next_pos_y += car.next_velocity_y * 0.1 + 0.5*car.next_acceleration_y*0.1**2

    @staticmethod
    def get_next_acceleration_velocity_position(car):
        Update.get_next_acceleration(car=car)
        Update.get_next_velocity(car=car)
        Update.get_next_position(car=car)

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
    def update_and_record_per_road(step,road,output_file):
        df = pd.DataFrame({})
        i = 0
        for vehicle in road.vehicles_list:
            if vehicle.depature_time < step:
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
                # print(df)
                df = pd.concat([df, new_df], ignore_index=True)
                Update.get_next_acceleration_velocity_position(car=vehicle)
                vehicle.update_acceleration_velocity_position()
        df.to_csv(
            output_file,
            mode="a",
            header=not os.path.exists(output_file),
            index=False
        )
        df = df.iloc[0:0]
    

    @staticmethod
    def multi_update_and_record_per_road(step,child_conn,output_file,road_idx):
        df = pd.DataFrame({})
        # serialized_data = child_conn.recv()
        # road = pickle.loads(serialized_data)
        road = Update.COMBINED_NET_FLOWS[road_idx]
        for vehicle in road.vehicles_list:
            if vehicle.depature_time < step:
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
                Update.get_next_acceleration_velocity_position(car=vehicle)
                vehicle.update_acceleration_velocity_position()

        df.to_csv(
            output_file,
            mode="a",
            header=not os.path.exists(output_file),
            index=False
        )
        df = df.iloc[0:0]
        # print("road size", sys.getsizeof(road))
        serialized_road = pickle.dumps(road)
        child_conn.send(serialized_road)
        child_conn.close()

        
    def update_and_record(self,output_file):
        step = self.step
        for road in self.combined_net_flows.values():
            Update.update_and_record_per_road(step,road,output_file)


    def multi_update_and_record(self,output_file):
        step = self.step
        pipes = []
        multi_process = []
        # multi_start_time = time.time()

        for road in self.combined_net_flows.values():
            parent_conn, child_conn = multiprocessing.Pipe()
            p = multiprocessing.Process(target=Update.multi_update_and_record_per_road, args=(step,child_conn,output_file, road.id))
            multi_process.append(p)
            p.start()
            # serialized_road = pickle.dumps(road)
            # print("dump", time.time() - multi_start_time)
            # parent_conn.send(serialized_road) # 发送数据消耗0.5s
            pipes.append(parent_conn)
        # print("for 1", time.time() - multi_start_time)
        for parent_conn in pipes:
            serialized_road = parent_conn.recv()
            road = pickle.loads(serialized_road)
            self.combined_net_flows[road.id] = road
        for process in multi_process:
            process.join()
        # multi_end_time = time.time()
        # delta_time = multi_end_time -multi_start_time
        # print(delta_time)