from datetime import datetime

from entity import Schedule


class ScheduleList:
    def __init__(self):
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
        return self.schedule_list.pop(0)

    def get_schedule_list(self):
        return self.schedule_list

    def update_schedule(self, n_time: datetime):
        if len(self.schedule_list) > 0:
            delta = n_time - self.schedule_list[0].start_time

            for schedule in self.schedule_list:
                schedule.start_time = schedule.start_time + delta
                schedule.end_time = schedule.end_time + delta
