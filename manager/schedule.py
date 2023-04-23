from entity import ScheduleList


class ScheduleManager:
    def __init__(self):
        self.schedule_lists: dict[str, ScheduleList] = dict()

    def init_schedule(self, v_name: str):
        self.schedule_lists[v_name] = ScheduleList()

    def get_schedule_lists(self):
        return self.schedule_lists

    def get_schedule_list(self, v_name: str):
        return self.schedule_lists[v_name]

    def get_log(self):
        schedule_logs = []

        for v_name in self.schedule_lists:
            schedule_list = self.schedule_lists[v_name]
            schedule_log = dict()
            schedule_log['v_name'] = v_name
            schedule_log['schedule'] = []

            if len(schedule_list) > 0:
                for schedule in schedule_list.get_schedule_list():
                    schedule_log['schedule'].append(schedule.get_log())

            schedule_logs.append(schedule_log)

        return schedule_logs