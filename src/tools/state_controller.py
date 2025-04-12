from src.vehicle.car import Car
from src.tools.calculate import Caculate
from src.road.base_road import BaseRoad
import src.tools.constant_values as params
from src.vehicle.base_vehicle import BaseVehicle
import numpy as np
import random

class StateController:
    STATESTABLE:dict = {
        "phase_0":{
            "start":0.0,
            "end":500.0
        },
        "phase_1":{
            "start":500.0,
            "end":1300.0
        },
        "phase_2":{
            "start":1300.0,
            "end":1400.0
        },
        "phase_3":{
            "start":1400.0,
            "end":1550.0
        }
    }

    def __init__(self):
        pass
    
    @staticmethod
    def is_which_phase(car):
        if (StateController.STATESTABLE["phase_0"]["start"] <= 
              car.current_pos_y < StateController.STATESTABLE["phase_0"]["end"]):
            return "phase_0"
        if (StateController.STATESTABLE["phase_1"]["start"] <= 
              car.current_pos_y < StateController.STATESTABLE["phase_1"]["end"]):
            return "phase_1"
        if (StateController.STATESTABLE["phase_2"]["start"] <= 
              car.current_pos_y < StateController.STATESTABLE["phase_2"]["end"]):
            return "phase_2"
        if (StateController.STATESTABLE["phase_3"]["start"] <= 
              car.current_pos_y < StateController.STATESTABLE["phase_3"]["end"]):
            return "phase_3"

    @staticmethod
    def get_state(car:Car):
        if StateController.is_which_phase(car) == "phase_0":
            if (car.on_which_road_id == "main_road_0" or 
                car.on_which_road_id == "main_road_1"):
                return "fric"
            if (car.on_which_road_id == "ramp_road"):
                return "free"
        if StateController.is_which_phase(car) == "phase_1":
            if (car.on_which_road_id == "main_road_0" or 
                car.on_which_road_id == "main_road_1"):
                return "lane_changed"
            if (car.on_which_road_id == "ramp_road"):
                return "free"
        if StateController.is_which_phase(car) == "phase_2":
            if car.on_which_road_id == "main_road_0":
                return "fric"
            if car.on_which_road_id == "main_road_1":
                return "lane_changed"
            if (car.on_which_road_id == "ramp_road"):
                return "free"
        if StateController.is_which_phase(car) == "phase_3":
            if (car.on_which_road_id == "main_road_0" or 
                car.on_which_road_id == "main_road_1"):
                return "compelled_lane_changed"
            if (car.on_which_road_id == "ramp_road"):
                if car.current_pos_y < 1535:
                    return "probably_lane_changed"
                else:
                    return "compelling_lane_changed"
    
    @staticmethod
    def fric_state(car):
        "主路车辆自由奔跑，只受附近车辆的斥力"
        all_force = Caculate.calculate_repulsion_force(car)
        all_force += Caculate.calculate_acceleration_willing(car_i=car)
        all_force += Caculate.calculate_centripetal_force(car_i=car)
        # print("fric",all_force)
        return all_force
    
    @staticmethod
    def free_state(car):
        "辅路车辆自由奔跑，只受附近车辆的斥力"
        all_force = Caculate.calculate_repulsion_force(car)
        all_force += Caculate.calculate_acceleration_willing(car_i=car)
        all_force += Caculate.calculate_centripetal_force(car_i=car)
        # print("free",all_force)
        return all_force
    
    @staticmethod
    def switch_to_which_lane(car:Car)->BaseRoad:
        if car.on_which_road_id == "main_road_0":
            return car.on_which_road.right_road
        if car.on_which_road_id == "main_road_1":
            return car.on_which_road.left_road
        if car.on_which_road_id == "acceleration_road":
            return car.on_which_road.left_road

    @staticmethod
    def probably_lane_changed(car):
        "主路车辆相互变道"
        all_force = Caculate.calculate_repulsion_force(car)
        all_force += Caculate.calculate_acceleration_willing(car_i=car)
        all_force += Caculate.calculate_centripetal_force(car_i=car)
        main_road = StateController.switch_to_which_lane(car) 
        if Caculate.main_find_closest_vehicles(main_vehicles = main_road.vehicles_list, car = car, rear_headway = params.Rear_Safe_headway):
            if random.random() <= params.RAO_MAIN:
                road = StateController.switch_to_which_lane(car=car)
                road.vehicles_list.append(car)
                car.on_which_road.vehicles_list.remove(car)
                car.on_which_road = road
                all_force += Caculate.calculate_centripetal_force(car_i=car)
        return all_force
    
    @staticmethod
    def lane_changed(car):
        "辅路车辆主动向主路变道"
        if car.on_which_road.left_road is not None:
            min_front_dist,min_rear_dist,front_headway,rear_headway = Caculate.ramp_find_nearest_car_besides_road(car_ramp = car,beside_road_vehicles = car.on_which_road.left_road.vehicles_list) 
            incentive = rear_headway >= params.T_sf
            safety = min_front_dist >= params.X_sf and min_rear_dist >= params.X_sf 
            if incentive and safety and random.random() <= params.RAO_RAMP:
                road = StateController.switch_to_which_lane(car=car)
                road.vehicles_list.append(car)
                car.on_which_road.vehicles_list.remove(car)
                car.on_which_road = road
                all_force  = Caculate.calculate_repulsion_force(car)
                all_force += Caculate.calculate_acceleration_willing(car_i=car)
                all_force += Caculate.calculate_centripetal_force(car_i=car)

            else:
                all_force  = Caculate.calculate_repulsion_force(car)
                all_force += Caculate.calculate_acceleration_willing(car_i=car)
                all_force += Caculate.calculate_centripetal_force(car_i=car)
            return all_force
        return np.array([[0.], [0.]])

    @staticmethod
    def compelling_lane_changed(car,virtual_obstacle):
        "辅路车辆强制变道"
        if car.on_which_road.left_road is not None:
            min_front_dist,min_rear_dist,front_headway,rear_headway = Caculate.ramp_find_nearest_car_besides_road(car_ramp = car,beside_road_vehicles = car.on_which_road.left_road.vehicles_list)
            incentive = rear_headway >= params.T_sf_xing
            safety = min_front_dist >= params.X_sf and min_rear_dist >= params.X_sf 
            if incentive and safety: 
                road = StateController.switch_to_which_lane(car=car)
                road.vehicles_list.append(car)
                car.on_which_road.vehicles_list.remove(car)
                car.on_which_road = road
                all_force  = Caculate.calculate_repulsion_force(car)
                all_force += Caculate.calculate_acceleration_willing(car_i=car)
                all_force += Caculate.calculate_centripetal_force(car_i=car)
            else:
                all_force  = Caculate.calculate_repulsion(car_i = car, car_k=virtual_obstacle , tao = 1.5, s_r = 10, x_xing = 5, c_2 = 6, c_3= 6)
                all_force += Caculate.calculate_repulsion_force(car)
                all_force += Caculate.calculate_acceleration_willing(car_i=car)
                all_force += Caculate.calculate_centripetal_force(car_i=car)
            return all_force
        return np.array([[0.], [0.]])

    @staticmethod
    def compelled_lane_changed(car:Car):
        "主路车辆被挤变道"
        all_force  = Caculate.calculate_repulsion_force(car)
        all_force += Caculate.calculate_acceleration_willing(car_i=car)
        all_force += Caculate.calculate_centripetal_force(car_i=car)
        if car.current_pos_x <= 3.75 or Caculate.main_find_closest_vehicles(main_vehicles = car.on_which_road.left_road.vehicles_list, car = car, rear_headway = params.Rear_Safe_headway):
            road = StateController.switch_to_which_lane(car=car)
            road.vehicles_list.append(car)
            car.on_which_road.vehicles_list.remove(car)
            car.on_which_road = road
            all_force += Caculate.calculate_centripetal_force(car_i=car)
        return all_force
    
    @staticmethod           
    def handle_state(car:Car):
        # print(StateController.get_state(car))
        match(StateController.get_state(car)):
            case "fric":
                return StateController.fric_state(car)
            case "free":
                return StateController.free_state(car)
            case "lane_changed":
                return StateController.lane_changed(car)
            case "probably_lane_changed":
                return StateController.probably_lane_changed(car)
            case "compelling_lane_changed":
                virtual_obstacle = BaseVehicle(
                    current_pos_y = 1550, 
                    current_pos_x = 8.75,
                    current_velocity_y = 0,
                    current_velocity_x = 0,
                    next_velocity_y = 0,
                    next_velocity_x = 0,
                    on_which_road_id = "obstacle",
                    on_which_road = None
                )
                return StateController.compelling_lane_changed(car,virtual_obstacle)
            case "compelled_lane_changed":
                return StateController.compelled_lane_changed(car)
            case _ :
                return np.array([[0.], [0.]])


