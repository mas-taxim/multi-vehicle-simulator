from datetime import datetime, timedelta
import logging
import random
import json
import pandas as pd
from tqdm import tqdm

from manager import TaskManager, VehicleManager, ScheduleManager

from graph.route import get_map, update_weight
from process.main_process import main_process, main_process_schedule


def init_log():
    log_time = datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"

    sys_logger = logging.getLogger("main")
    sys_logger.setLevel(logging.WARNING)

    # log 출력
    sys_log_handler = logging.FileHandler(f'sys_log/{log_time}')
    sys_log_handler.setFormatter(
        logging.Formatter('%(levelname)s - %(message)s'))
    sys_logger.addHandler(sys_log_handler)


def run():
    init_log()

    random.seed(0)

    graph_name = 'seoul_default_0_1_link'
    nodes, node_idx, graph = get_map(graph_name)

    df_task = pd.read_csv('data/reqeust_200108.csv')
    df_task = df_task.sample(100, random_state=0)
    df_task['move_time'] = pd.to_datetime(df_task['end_time']) - pd.to_datetime(df_task['start_time'])
    df_task = df_task.sort_values('req_time')
    df_task.reset_index(drop=True, inplace=True)
    df_task = df_task[['req_time', 'start_node', 'end_node', 'move_time']]
    # print(df_task)

    tasks = []
    for i, row in df_task.iterrows():
        tasks.append((row['req_time'], row['start_node'], row['end_node']))

    vehicle_mgr: VehicleManager = VehicleManager()

    vehicles_run_time = []
    vehicles_run_time.extend([0, 26] for _ in range(10))

    schedule_mgr: ScheduleManager = ScheduleManager()

    for i in range(len(vehicles_run_time)):
        v_name = "V" + str(i)
        vehicle_mgr.add_vehicle(v_name, nodes[3878][0], nodes[3878][1])
        schedule_mgr.init_schedule(v_name)

    task_mgr: TaskManager = TaskManager()

    logs = []
    schedule_logs = []
    n_time: datetime = datetime.strptime("2023-02-02", '%Y-%m-%d')
    for h in range(0, 15):
        print(h)
        update_weight(graph_name, h % 24 + 1)

        for i, run_time in enumerate(vehicles_run_time):
            if run_time[0] == h:
                vehicle_mgr.open_vehicle("V" + str(i), n_time + timedelta(hours=run_time[1] - run_time[0]))
            if run_time[1] == h:
                vehicle_mgr.close_vehicle("V" + str(i))

        for m in range(60):
            n_time += timedelta(minutes=1)

            log, schedule_log = main_process_schedule(n_time, graph_name, vehicle_mgr, task_mgr, schedule_mgr, tasks)
            logs.append(log)
            if len(schedule_log) > 0:
                schedule_logs.append(schedule_log)

            # logs.append(main_process(n_time, graph_name, vehicle_mgr, task_mgr, tasks))

    print("left task in wait queue")
    print(task_mgr.wait_queue)
    json_obj = {'logs': logs,
                'schedules': schedule_logs}

    log_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'log/{log_time}.json', 'w') as outfile:
        json.dump(json_obj, outfile, indent=4)


if __name__ == "__main__":
    run()
