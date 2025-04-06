class Update:
    def __init__(
        self,
        combined_net_flows
    ) -> None:
        self.combined_net_flows = combined_net_flows

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
    
    def sort_and_assign(self):
        for value in self.combined_net_flows.values():
            sorted_vehicle = sorted(value.vehicles_list, key=lambda vehicle: vehicle.current_pos_y)
            Update.assign_leaders_and_followers(vehicles = sorted_vehicle)

    def get_step(self,step):
        self.step = step

    def unpdate_all(self):
        pass