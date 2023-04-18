import networkx as nx
from datetime import datetime, timedelta

from entity import Task, Vehicle, Location, Schedule
from graph.route import get_map
from manager import VehicleManager

schedules = dict()


def init_schedule(v_name: str):
    schedules[v_name] = []


def get_schedule(v_name: str):
    return schedules[v_name]


def add_schedule(n_time: datetime, graph_name: str, vehicle: Vehicle, task: Task):
    node, node_idx, graph = get_map(graph_name)

    v_name = vehicle.name
    schedule = schedules[v_name]

    # load 지점까지 움직이는 schedule
    if len(schedule) == 0:
        start_loc: Location = Location(vehicle.loc.x, vehicle.loc.y)
        start_time: datetime = n_time
    else:
        start_loc: Location = Location(schedule[-1].end_loc.x, schedule[-1].end_loc.y)
        start_time: datetime = schedule[-1].end_time

    end_loc: Location = Location(task.loc_load.x, task.loc_load.y)

    move_load_time: int = nx.shortest_path_length(graph, node_idx[(start_loc.x, start_loc.y)], node_idx[(
        end_loc.x, end_loc.y)], weight='weight')

    end_time: datetime = start_time + timedelta(minutes=move_load_time)

    schedule.append(Schedule(-1, start_time, start_loc, end_time, end_loc))

    # unload 지점까지 움직이는 schedule
    start_loc = Location(end_loc.x, end_loc.y)
    start_time = end_time

    end_loc = Location(task.loc_unload.x, task.loc_unload.y)

    move_unload_time: int = nx.shortest_path_length(graph, node_idx[(start_loc.x, start_loc.y)], node_idx[(
        end_loc.x, end_loc.y)], weight='weight')

    end_time: datetime = start_time + timedelta(minutes=move_unload_time)

    schedule.append(Schedule(task.idx, start_time, start_loc, end_time, end_loc))


def get_earliest_vehicle(n_time: datetime, graph_name: str, vehicle_mgr: VehicleManager, task: Task) -> Vehicle:
    node, node_idx, graph = get_map(graph_name)

    min_sched_load_time: datetime = n_time + timedelta(hours=240)
    min_vehicle: Vehicle = None

    move_unload_time = nx.shortest_path_length(graph, node_idx[(task.loc_load.x, task.loc_load.y)], node_idx[(
        task.loc_unload.x, task.loc_unload.y)], weight='weight')

    for v_name in vehicle_mgr.vehicles:
        vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)
        schedule = schedules[v_name]

        if len(schedule) == 0:
            last_sched_time = n_time
            last_loc = vehicle.loc
        else:
            last_sched_time = schedule[-1].end_time
            last_loc = schedule[-1].end_loc

        if vehicle.running and vehicle.close_time > last_sched_time:
            move_load_time = nx.shortest_path_length(graph, node_idx[(last_loc.x, last_loc.y)], node_idx[(
                task.loc_load.x, task.loc_load.y)], weight='weight')
            sched_load_time = last_sched_time + timedelta(minutes=move_load_time)
            sched_unload_time = sched_load_time + timedelta(minutes=move_unload_time)

            if vehicle.close_time > sched_unload_time:
                if min_sched_load_time > sched_load_time:
                    min_sched_load_time = sched_load_time
                    min_vehicle = vehicle

    return min_vehicle
