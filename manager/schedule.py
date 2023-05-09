from entity import ScheduleList


class ScheduleManager:
    def __init__(self):
        self.schedule_lists: dict[str, ScheduleList] = dict()
        self.pre_schedule_lists: dict[str, ScheduleList] = dict()

    def init_schedule(self, v_name: str):
        self.schedule_lists[v_name] = ScheduleList()

    def get_schedule_lists(self):
        return self.schedule_lists

    def get_schedule_list(self, v_name: str):
        return self.schedule_lists[v_name]

    def record_to_pre_schedule_lists(self):
        self.pre_schedule_lists = self.schedule_lists

    def clear_schedule_lists(self) -> list:
        """
        Clear all Schedule List without Running Schedule
        """

        cleared_task_list = []
        # cleared_task_list = dict()
        self.record_to_pre_schedule_lists()
        for sched_list in self.schedule_lists.values():
            if sched_list.__len__() == 0:
                continue
            cleared_task_list += sched_list.clear_schedule_list()
            # cleared_task_list = {**cleared_task_list, **sched_list.clear_schedule_list()} ## clear and append

        return cleared_task_list

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
