import numpy as np
class Caculate:
    @staticmethod
    def get_vehicle_current_scalar_acceleration(car:object) -> float:
        return np.sqrt(car.current_acceleration_x**2 + car.current_acceleration_y**2)

    @staticmethod
    def get_vehicle_current_scalar_speed(car:object) -> float:
        return np.sqrt(car.current_velocity_x**2 + car.current_velocity_y**2)
    
    @staticmethod
    # k 为前车，i 为后车
    def calculate_repulsion(car_i,car_k,tao,s_r,x_xing,c_2,c_3):
        car_i_v = Caculate.get_vehicle_current_scalar_speed(car_i)
        q_v = (car_i_v * tao + s_r)/x_xing
        Q = np.array([[1, 0], [0, q_v]])
        Q_ni = np.linalg.inv(Q)
        x_k = np.array([[car_k.current_pos_x - car_k.car_width / 2],[car_k.current_pos_y - car_k.car_length / 2]])
        x_i = np.array([[car_i.current_pos_x - car_i.car_width / 2],[car_i.current_pos_y - car_i.car_length / 2]] )
        v_i = np.array([[car_i.current_velocity_x], [car_i.current_velocity_y]])
        v_k = np.array([[car_k.current_velocity_x], [car_k.current_velocity_y]])
        r_ik = np.dot(Q_ni, x_k - x_i)
        r_ik_dw = r_ik / np.linalg.norm(r_ik) if np.linalg.norm(r_ik) != 0 else r_ik
        delta_v_ik = np.dot(np.transpose(np.dot(Q_ni, v_k - v_i)), r_ik_dw)
        fr_ik = np.dot(Q , r_ik_dw)*min(0,delta_v_ik*c_2 + c_3*(np.linalg.norm(r_ik)-x_xing))
        return fr_ik
    
    @staticmethod
    def calculate_acceleration_willing(car_i,v_max,c_1):
        return np.array([[0],[(v_max - car_i.current_velocity_y)*c_1]])
    
    @staticmethod
    def calculate_centripetal_force(car_i,k_1,k_2,current_central_line):
        return np.array([[-car_i.current_velocity_x*k_1 - (car_i.current_pos_x-current_central_line)*k_2],[0]])
    
