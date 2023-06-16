from ..entity import ScheduleList


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

    def swap(self, graph_name, v_name1, idx1, v_name2, idx2):
        schedule_list1 = self.schedule_lists[v_name1].get_schedule_list()
        schedule_list2 = self.schedule_lists[v_name2].get_schedule_list()

        temp_schedule = schedule_list1[idx1]
        schedule_list1[idx1] = schedule_list2[idx2]
        schedule_list2[idx2] = temp_schedule

        self.schedule_lists[v_name1].update_schedule_from_start(graph_name)
        self.schedule_lists[v_name2].update_schedule_from_start(graph_name)

    def get_logs(self):
        schedule_logs = []

        for v_name in self.schedule_lists:
            schedule_list = self.schedule_lists[v_name]
            schedule_log = dict()
            schedule_log['vehicle_id'] = v_name
            schedule_log['prev_schedules'] = []
            schedule_log['schedules'] = []

            if len(schedule_list.get_schedule_list_all()) > 0:
                for schedule in schedule_list.get_schedule_list_all():
                    if schedule.status == 0:
                        schedule_log['prev_schedules'].append(schedule.task_id)
                    else:
                        schedule_log['schedules'].append(schedule.get_log())

            schedule_logs.append(schedule_log)

        return schedule_logs
