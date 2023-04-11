from datetime import datetime, timedelta
import logging
import random
import json

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

    graph_name = 'seoul'
    nodes, node_idx, graph = get_map(graph_name)

    vehicle_mgr: VehicleManager = VehicleManager()

    vehicles_run_time = []
    vehicles_run_time.extend([0, 7] for _ in range(3))
    vehicles_run_time.extend([7, 13] for _ in range(5))
    vehicles_run_time.extend([9, 18] for _ in range(10))
    vehicles_run_time.extend([16, 24] for _ in range(3))
    vehicles_run_time.extend([24, 30] for _ in range(5))

    for i in range(len(vehicles_run_time)):
        vehicle_mgr.add_vehicle("V" + str(i), nodes[3878][0], nodes[3878][1])

    task_mgr: TaskManager = TaskManager()

    logs = []
    n_time: datetime = datetime.strptime("2023-02-02", '%Y-%m-%d')
    for h in range(0, 30):
        print(h)
        update_weight(graph_name, h % 24 + 1)

        for i, run_time in enumerate(vehicles_run_time):
            if run_time[0] == h:
                vehicle_mgr.open_vehicle("V" + str(i))
            if run_time[1] == h:
                vehicle_mgr.close_vehicle("V" + str(i))

        for m in range(60):
            n_time += timedelta(minutes=1)
            logs.append(main_process(n_time, graph_name, vehicle_mgr, task_mgr))

            if h < 6:
                set_epsilon(random.random() * 0.05)
            elif 6 <= h < 8:
                set_epsilon(random.random() * 0.1)
            elif 8 <= h < 10:
                set_epsilon(random.random() * 0.3)
            elif 10 <= h < 14:
                set_epsilon(random.random() * 0.15)
            elif 14 <= h < 16:
                set_epsilon(random.random() * 0.2)
            elif 16 <= h < 19:
                set_epsilon(random.random() * 0.3)
            elif 19 <= h < 21:
                set_epsilon(random.random() * 0.15)
            elif 21 <= h < 24:
                set_epsilon(random.random() * 0.05)
            else:
                set_epsilon(random.random() * 0)

    print(task_mgr.wait_queue)
    json_obj = {'logs': logs}

    log_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'log/{log_time}.json', 'w') as outfile:
        json.dump(json_obj, outfile, indent=4)


if __name__ == "__main__":
    run()
