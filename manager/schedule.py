class ScheduleManager:
    def __init__(self):
        self.schedules: dict[str, list] = dict()

    def init_schedule(self, v_name: str):
        self.schedules[v_name] = []

    def get_schedules(self):
        return self.schedules

    def get_schedule(self, v_name: str):
        return self.schedules[v_name]

    def print(self):
        for v_name in self.schedules:
            schedule = self.schedules[v_name]

            if len(schedule) > 0:
                print(v_name, schedule)
