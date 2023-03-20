from datetime import datetime, timedelta
import logging
import random
import json

from manager import TaskManager, VehicleManager

from graph.route import get_graph
from process.main_process import main_process, set_epsilon
from process.generate_process import generate_task


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

    n_time: datetime = datetime.strptime("2023-02-02", '%Y-%m-%d')

    graph_name = 'seoul_gu'
    node, node_idx, graph = get_graph(graph_name)

    vehicle_mgr: VehicleManager = VehicleManager()
    vehicle_mgr.add_vehicle("V1", node[0][0], node[0][1])
    vehicle_mgr.add_vehicle("V2", node[0][0], node[0][1])
    vehicle_mgr.add_vehicle("V3", node[0][0], node[0][1])

    task_mgr: TaskManager = TaskManager()

    generate_task(n_time, node, task_mgr)


    logs = []
    for i in range(24 * 60):
        n_time += timedelta(minutes=1)
        logs.append(main_process(n_time, graph_name, vehicle_mgr, task_mgr))
        set_epsilon(random.random() * 0.04)
        
    json_obj = {'logs': logs}

    log_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'log/{log_time}.json', 'w') as outfile:
        json.dump(json_obj, outfile, indent=4)


if __name__ == "__main__":
    run()
