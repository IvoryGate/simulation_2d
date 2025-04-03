class Loop:
    START_TIME:float = 0.0,
    END_TIME:float = 3600.0,
    PER_STEP:float = 0.1

    def __init__(
        self,
        start_time:float = START_TIME,
        end_time:float = END_TIME,
        per_step:float = PER_STEP 
    ):
        self.start_time = start_time,
        self.end_time = end_time,
        self.per_step = per_step

    @staticmethod
    def float_range(start, stop, step):
        while start < stop:
            yield start
            start += step

    def load_config():
        pass

    def load_net():
        pass

    def entry_simulation(self):
        for step in Loop.float_range(self.start_time,self.end_time,self.per_step):
            pass           
