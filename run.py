from datetime import datetime, timedelta
import logging
import random
import json
import pandas as pd
from tqdm import tqdm

from manager import TaskManager, VehicleManager

from graph.route import get_map, update_weight
from process.main_process import main_process, set_epsilon


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

    graph_name = 'seoul_link_j'
    nodes, node_idx, graph = get_map(graph_name)

    df_task = pd.read_csv('./data/reqeust_200108.csv')
    df_task = df_task[['req_time', 'start_node', 'end_node']]

    tasks = []
    for i, row in df_task.iterrows():
        tasks.append((row['req_time'], row['start_node'], row['end_node']))

    vehicle_mgr: VehicleManager = VehicleManager()

    vehicles_run_time = []
    vehicles_run_time.extend([0, 7] for _ in range(30))
    vehicles_run_time.extend([7, 16] for _ in range(140))
    vehicles_run_time.extend([8, 17] for _ in range(140))
    vehicles_run_time.extend([10, 20] for _ in range(140))
    vehicles_run_time.extend([20, 30] for _ in range(30))

    for i in range(len(vehicles_run_time)):
        vehicle_mgr.add_vehicle("V" + str(i), nodes[3878][0], nodes[3878][1])

    task_mgr: TaskManager = TaskManager()

    logs = []
    n_time: datetime = datetime.strptime("2023-02-02", '%Y-%m-%d')
    for h in tqdm(range(0, 30), position=0, desc="hour : "):
        update_weight(graph_name, h % 24 + 1)

        for i, run_time in enumerate(vehicles_run_time):
            if run_time[0] == h:
                vehicle_mgr.open_vehicle("V" + str(i))
            if run_time[1] == h:
                vehicle_mgr.close_vehicle("V" + str(i))

        for m in tqdm(range(60), position=1, leave=False, desc="minute : "):
            n_time += timedelta(minutes=1)
            logs.append(main_process(n_time, graph_name,
                        vehicle_mgr, task_mgr, tasks))

    print("left task in wait queue")
    print(task_mgr.wait_queue)
    json_obj = {'logs': logs}

    log_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'log/{log_time}.json', 'w') as outfile:
        json.dump(json_obj, outfile, indent=4)


if __name__ == "__main__":
    run()
