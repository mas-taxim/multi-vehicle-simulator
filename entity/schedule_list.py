from datetime import datetime

from entity import Schedule


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

    def update_schedule(self, n_time: datetime):
        if len(self.schedule_list) > 0:
            delta = n_time - self.schedule_list[0].start_time

            for schedule in self.schedule_list:
                schedule.start_time = schedule.start_time + delta
                schedule.load_time = schedule.load_time + delta
                schedule.unload_time = schedule.unload_time + delta
