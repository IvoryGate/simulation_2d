# class
## BaseVehicle

`BaseVehicle` 是车辆的基类，包含所有车辆共有的方法属性。不同的车辆均继承于这个类。

```mermaid
classDiagram
      BaseVehicle : +String id
      BaseVehicle : -float depature_time
      BaseVehicle : -float current_pos_x
      BaseVehicle : -float current_pos_y
      BaseVehicle : -float current_velocity_x
      BaseVehicle : -float current_velocity_y
      BaseVehicle : -float current_acceleration_x
      BaseVehicle : -float current_acceleration_y
      BaseVehicle : -float next_pos_x
      BaseVehicle : -float next_pos_y
      BaseVehicle : -float next_velocity_x
      BaseVehicle : -float next_velocity_y
      BaseVehicle : -float next_acceleration_x
      BaseVehicle : -float next_acceleration_y
      BaseVehicle : -Road on_which_road
      
```

## Car

```mermaid
classDiagram
    BaseVehicle : +String id
    BaseVehicle : -float depature_time
    BaseVehicle : -float current_pos_x
    BaseVehicle : -float current_pos_y
    BaseVehicle : -float current_velocity_x
    BaseVehicle : -float current_velocity_y
    BaseVehicle : -float current_acceleration_x
    BaseVehicle : -float current_acceleration_y
    BaseVehicle : -float next_pos_x
    BaseVehicle : -float next_pos_y
    BaseVehicle : -float next_velocity_x
    BaseVehicle : -float next_velocity_y
    BaseVehicle : -float next_acceleration_x
    BaseVehicle : -float next_acceleration_y
    BaseVehicle : -Road on_which_road
    BaseVehicle : +obj leader
    BaseVehicle : +obj follower
      
	BaseVehicle <-- Car
	Car : +float car_length
	Car : +float car_width
	
```



## BaseRoad

`Road`包含该路段的相关信息。

```mermaid
classDiagram
	Road : +String id
	Road : +float central_line
	Road : +float road_length
	Road : +float road_width
	Road : +float max_allowed_speed
	Road : +list[Car] vehicles_list
	
```



## RampRoad

`RampRoad`继承自`BaseRoad`类，除了该路段的基本属性方法外，还包括匝道部分。

# files



