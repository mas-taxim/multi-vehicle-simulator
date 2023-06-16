from datetime import datetime, timedelta

from entity import Schedule
from graph.map import get_map
from graph.route import get_distance


class ScheduleList:
    def __init__(self):
        self.terminated_list: list[Schedule] = []
        self.schedule_list: list[Schedule] = []

    def __len__(self):
        return len(self.schedule_list)

    def add_schedule(self, schedule: Schedule):
        self.schedule_list.append(schedule)

    def get_schedule(self, index):
        return self.schedule_list[index]

    def get_last_schedule(self):
        return self.schedule_list[-1]

    def pop_schedule(self):
        schedule = self.schedule_list.pop(0)
        schedule.set_status(Schedule.TERMINATED)
        self.terminated_list.append(schedule)

        return schedule

    def get_schedule_list_all(self):
        schedule_list_all = []
        schedule_list_all.extend(self.terminated_list)
        schedule_list_all.extend(self.schedule_list)

        return schedule_list_all

    def get_schedule_list(self):
        return self.schedule_list

    def update_schedules(self, n_time: datetime):
        if len(self.schedule_list) > 0:
            delta = n_time - self.schedule_list[0].start_time

            for schedule in self.schedule_list:
                schedule.start_time = schedule.start_time + delta
                schedule.load_time = schedule.load_time + delta
                schedule.unload_time = schedule.unload_time + delta

    def update_schedule_from_start(self, graph_name):
        node, node_idx, graph = get_map(graph_name)

        for i in range(1, len(self.schedule_list)):
            prev_schedule = self.schedule_list[i - 1]
            now_schedule = self.schedule_list[i]

            now_schedule.start_loc.x = prev_schedule.unload_loc.x
            now_schedule.start_loc.y = prev_schedule.unload_loc.y

            move_load_time = get_distance(graph_name, node_idx[now_schedule.start_loc.get_tuple()],
                                          node_idx[now_schedule.load_loc.get_tuple()])
            move_unload_time = get_distance(graph_name, node_idx[now_schedule.load_loc.get_tuple()],
                                            node_idx[now_schedule.unload_loc.get_tuple()])

            now_schedule.start_time = prev_schedule.unload_time
            now_schedule.load_time = now_schedule.start_time + timedelta(
                minutes=move_load_time + now_schedule.task_elapsed_time + 3)
            now_schedule.unload_time = now_schedule.load_time + timedelta(
                minutes=move_unload_time + now_schedule.task_elapsed_time + 3)

    def clear_schedule_list(self) -> list:
        if len(self.schedule_list) == 0:
            return

        cleared_task_list = []
        # cleared_task_list = dict()
        running_schedule = None
        if self.schedule_list[0].status == Schedule.RUNNING:
            running_schedule = self.schedule_list.pop(0)

        for schedule in self.schedule_list:
            cleared_task_list.append(schedule.task_id)
            # cleared_task_list[schedule.task_id] = False

        # if running schedule exist, keep this schedule
        self.schedule_list: list[Schedule] = []
        if running_schedule is not None:
            self.schedule_list.append(running_schedule)

        return cleared_task_list
