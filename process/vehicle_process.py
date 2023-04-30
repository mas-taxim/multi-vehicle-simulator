import logging
import math
from datetime import datetime, timedelta

from entity import Path, Task, Vehicle, Location, ScheduleList
from entity.location import is_same_location
from manager import VehicleManager, ScheduleManager

logger = logging.getLogger("main")


def vehicle_process(n_time: datetime, vehicle_mgr: VehicleManager, schedule_mgr: ScheduleManager = None):
    for v_name in vehicle_mgr.vehicles:
        vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)

        if schedule_mgr is not None:
            schedule_list = schedule_mgr.get_schedule_list(v_name)
        else:
            schedule_list = None

        task: Task = vehicle_mgr.get_alloced_task(v_name)

        if vehicle.status == Vehicle.WAIT:
            pass
        elif vehicle.status == Vehicle.ALLOC:
            alloc(n_time, vehicle, task)
        elif vehicle.status == Vehicle.MOVE_TO_LOAD:
            move_to_load(n_time, vehicle, task)
        elif vehicle.status == Vehicle.LOAD_START:
            load_start(n_time, vehicle, task)
        elif vehicle.status == Vehicle.LOADING:
            loading(n_time, vehicle, task)
        elif vehicle.status == Vehicle.LOAD_END:
            load_end(n_time, vehicle, task)
        elif vehicle.status == Vehicle.MOVE_TO_UNLOAD:
            move_to_unload(n_time, vehicle, task)
        elif vehicle.status == Vehicle.UNLOAD_START:
            unload_start(n_time, vehicle, task)
        elif vehicle.status == Vehicle.UNLOADING:
            unloading(n_time, vehicle, task)
        elif vehicle.status == Vehicle.UNLOAD_END:
            unload_end(n_time, vehicle, task, schedule_list)
        elif vehicle.status == Vehicle.CLOSE:
            close(n_time, vehicle, task)
        else:
            logger.error(
                f"[vehicle_process] Exception occurred in the status of vehicle -> name:{vehicle.name}, status:{vehicle.status}")


def move_origin(vehicle: Vehicle, path: Path = None):
    '''
    걸리는 시간이 dest 와 arrive의 Euclidean distance로 계산되고 있음.
    move time 정의 -> dest 와 arrive Euclidean distance * weight 값으로 표현
    '''
    if path is None:
        if vehicle.route:
            path = vehicle.route[0]
        else:
            logger.error(
                f"[move] vehicle's route is empty -> name:{vehicle.name}")

    depart = path.depart_loc
    arrive = path.arrive_loc

    unit_distance = (math.sqrt((arrive.x - depart.x) ** 2 +
                               (arrive.y - depart.y) ** 2)) / path.weight
    length = math.sqrt((arrive.x - vehicle.loc.x) ** 2 +
                       (arrive.y - vehicle.loc.y) ** 2)

    # 소수점으로 인해 1번 더 움직이는 것을 막기 위해 마지막에 0.0001 더하고 비교
    if length < unit_distance + 0.0001:
        vehicle.loc.x = arrive.x
        vehicle.loc.y = arrive.y
    else:
        vehicle.loc.x += (arrive.x - vehicle.loc.x) / length * unit_distance
        vehicle.loc.y += (arrive.y - vehicle.loc.y) / length * unit_distance

    if is_same_location(vehicle.loc, arrive) and len(vehicle.route) > 1:
        vehicle.route.pop(0)


def move(vehicle: Vehicle, final_destination: Location, path: Path = None):
    left_time = 60.0
    # depart: Location = vehicle.loc
    # arrive: Location = vehicle.loc

    # update path info
    while len(vehicle.route) > 0:
        path = vehicle.route[0]
        depart = path.depart_loc
        arrive = path.arrive_loc

        if is_same_location(arrive, depart):
            vehicle.route.pop(0)
            if len(vehicle.route) == 0:
                print("[ERROR] CASE 4")
            continue
        else:
            break

    while left_time > 0:
        unit_distance = (math.sqrt((arrive.x - depart.x) ** 2 +
                                   (arrive.y - depart.y) ** 2)) / (path.weight * 60)
        length = math.sqrt((arrive.x - vehicle.loc.x) ** 2 +
                           (arrive.y - vehicle.loc.y) ** 2)

        """
        for debuging, after must delete
        print("----------------------------")
        print(f"vehicle name : {vehicle.name}")
        print(f"left time : {left_time}")
        print(f"unit distance : {unit_distance}")
        print(f"left length : {length}")
        print(f"path weight : {path.weight}")
        print(f"depart : {path.depart_loc}")
        print(f"arrive : {path.arrive_loc}")
        print(f"path : {vehicle.route[0:4]}")
        print(f"final dest : {final_destination}")
        """

        # arrive == depart
        if is_same_location(depart, arrive):
            if vehicle.route:
                path = vehicle.route[0]
            else:
                logger.error(
                    f"[move] vehicle's route is empty[case0] -> name:{vehicle.name}")

        # move over 1path
        if unit_distance * left_time >= length:
            left_time -= length / unit_distance  # decrease spend time

            # update vehicle loc to arrive
            # TODO: vehicle.loc = arrive : 이거 왜 안쓰고 두개로 나눠서 대입하는지 확인필요
            vehicle.loc.x = arrive.x
            vehicle.loc.y = arrive.y

            # delete path info
            if len(vehicle.route) > 0:
                vehicle.route.pop(0)
            else:
                logger.error(
                    f"[move] vehicle's route is empty [case1] -> name:{vehicle.name}")
                print("[ERROR] left Path is not exist")

            # arrive final destination.
            if is_same_location(vehicle.loc, final_destination):
                # print("[INFO] arrive final dest")
                return

            # for logging
            if len(vehicle.route) == 0:
                logger.error(
                    f"[move] vehicle's route is empty [case2] -> name:{vehicle.name}")
                print("[ERROR] left Path is not exist")

            # update path info
            while len(vehicle.route) > 0:
                path = vehicle.route[0]
                depart = path.depart_loc
                arrive = path.arrive_loc

                if is_same_location(arrive, depart):
                    vehicle.route.pop(0)
                    continue
                else:
                    break

            continue

        # move under 1path each
        vehicle.loc.x += (arrive.x - vehicle.loc.x) / \
                         length * unit_distance * left_time
        vehicle.loc.y += (arrive.y - vehicle.loc.y) / \
                         length * unit_distance * left_time
        left_time = 0


def alloc(n_time: datetime, vehicle: Vehicle, task: Task):
    vehicle.status = Vehicle.MOVE_TO_LOAD
    task.status = Task.MOVE_TO_LOAD


def move_to_load(n_time: datetime, vehicle: Vehicle, task: Task):
    if not is_same_location(vehicle.loc, task.loc_load):
        # print("\n====MOVE TO LOAD====")
        move(vehicle, task.loc_load)
    else:
        vehicle.status = Vehicle.LOAD_START
        task.status = Task.LOAD_START

        task.load_start_time = n_time


def load_start(n_time: datetime, vehicle: Vehicle, task: Task):
    vehicle.status = Vehicle.LOADING
    task.status = Task.LOADING


def loading(n_time: datetime, vehicle: Vehicle, task: Task):
    if task.load_start_time + timedelta(minutes=task.elapsed_time) >= n_time:
        pass
    else:
        vehicle.status = vehicle.LOAD_END
        task.status = Task.LOAD_END

        task.load_end_time = n_time


def load_end(n_time: datetime, vehicle: Vehicle, task: Task):
    vehicle.status = Vehicle.MOVE_TO_UNLOAD
    task.status = Task.MOVE_TO_UNLOAD


def move_to_unload(n_time: datetime, vehicle: Vehicle, task: Task):
    if not is_same_location(vehicle.loc, task.loc_unload):
        # print("\n====MOVE TO UNLOAD====")
        move(vehicle, task.loc_unload)
    else:
        vehicle.status = Vehicle.UNLOAD_START
        task.status = Task.UNLOAD_START
        task.unload_start_time = n_time


def unload_start(n_time: datetime, vehicle: Vehicle, task: Task):
    vehicle.status = Vehicle.UNLOADING
    task.status = Task.UNLOADING


def unloading(n_time: datetime, vehicle: Vehicle, task: Task):
    if task.unload_start_time + timedelta(minutes=task.elapsed_time) >= n_time:
        pass
    else:
        vehicle.status = Vehicle.UNLOAD_END
        task.status = Task.UNLOAD_END
        task.unload_end_time = n_time


def unload_end(n_time: datetime, vehicle: Vehicle, task: Task, schedule_list: ScheduleList):
    if vehicle.running:
        vehicle.status = Vehicle.WAIT
    else:
        vehicle.status = Vehicle.CLOSE

    if schedule_list is not None:
        schedule = schedule_list.pop_schedule()
        schedule.load_time = task.load_end_time
        schedule.unload_time = n_time

        schedule_list.update_schedule(n_time)

    vehicle.route = []


def close(n_time: datetime, vehicle: Vehicle, task: Task):
    if vehicle.running:
        vehicle.status = Vehicle.WAIT
    else:
        vehicle.status = Vehicle.CLOSE
