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

    def get_logs(self):
        schedule_logs = []

        for v_name in self.schedule_lists:
            schedule_list = self.schedule_lists[v_name]
            schedule_log = dict()
            schedule_log['vehicle_id'] = v_name
            schedule_log['schedules'] = []

            if len(schedule_list.get_schedule_list_all()) > 0:
                for schedule in schedule_list.get_schedule_list_all():
                    schedule_log['schedules'].append(schedule.get_log())

            schedule_logs.append(schedule_log)

        return schedule_logs
