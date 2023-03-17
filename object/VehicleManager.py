import logging

from object.Vehicle import Vehicle
from object.Task import Task

logger = logging.getLogger("main")


class VehicleManager:
    def __init__(self):
        self.vehicles: dict[str, Vehicle] = dict()
        self.tasks_alloced: dict[str, Task] = dict()

    def get_vehicle(self, v_name: str):
        if v_name in self.vehicles:
            return self.vehicles[v_name]
        else:
            logger.error(f"[get_vehicle] v_name does not exist -> v_name:{v_name}")

    def add_vehicle(self, v_name: str, init_x: float = 37.52897, init_y: float = 126.917101):
        if v_name in self.vehicles:
            logger.error(f"[add_vehicle] v_name already exist -> v_name:{v_name}")
        else:
            self.vehicles[v_name] = Vehicle(v_name)
            self.tasks_alloced[v_name] = None
            self.vehicles[v_name].loc.x = init_x
            self.vehicles[v_name].loc.y = init_y

    def get_alloced_task(self, v_name):
        ''' v_name에 할당되어있는 task를 반환, 존재하지 않을경우 None '''
        if v_name in self.vehicles:
            return self.tasks_alloced.get(v_name)
        else:
            logger.error(f"[get_vehicle] v_name does not exist -> v_name:{v_name}")
        return None

    def reset_alloced_task(self, v_name):
        self.tasks_alloced[v_name] = None

    def alloc_task(self, v_name: str, task: Task):
        if v_name in self.vehicles:
            self.tasks_alloced[v_name] = task
        else:
            logger.error(f"[get_vehicle] v_name does not exist -> v_name:{v_name}")

    def get_idx_task_alloced(self):
        idx_list = []

        for v_name in self.tasks_alloced:
            if self.tasks_alloced[v_name] is None:
                idx_list.append((v_name, None))
            else:
                idx_list.append((v_name, self.tasks_alloced[v_name].idx))

        return idx_list

    def get_log(self):
        vehicle_logs = []

        for v_name in self.vehicles:
            vehicle: Vehicle = self.get_vehicle(v_name)
            vehicle_log = vehicle.get_log()
            vehicle_log['allocated_id'] = (
                self.tasks_alloced[v_name].idx if self.tasks_alloced[v_name] is not None else None)

            vehicle_logs.append(vehicle_log)

        return vehicle_logs
