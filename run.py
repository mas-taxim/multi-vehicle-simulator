from datetime import datetime, timedelta
import logging
import random
import json
import time
import pandas as pd
from tqdm import tqdm

from manager import TaskManager, VehicleManager, ScheduleManager

from graph.map import get_map, update_weight
from process.main_process import main_process, main_process_schedule

# file Name Setting
graph_name = '20230426_seoul_default_0_7_st_link'
request_date = '20200829'
request_name = 'reqeust_2020-08-29_20230426_seoul_default_0_5_link.csv'

# Mode Setting
schedule_type = "dispatch"
# schedule_type = "reschedule"
# schedule_type = "swap"
simulation_time = 24
simulation_vehicle_num = 2
simulation_task_num = 20
simulation_reschedule_time = 10


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

    print("============ Simulation Start ============")
    start_time = time.time()

    # init setting
    init_log()
    random.seed(0)

    # Graph Setting
    nodes, node_idx, graph = get_map(graph_name)

    # Task Setting
    df_task = pd.read_csv(f'data/{request_name}')
    print(f"Total Task Data Num : {len(df_task)}")
    df_task = df_task.sample(simulation_task_num, random_state=0)  # random sampling for test
    print(f"Sample Task Data Num : {len(df_task)}")

    df_task['move_time'] = pd.to_datetime(df_task['end_time']) - pd.to_datetime(df_task['start_time'])
    df_task = df_task.sort_values('req_time')
    df_task.reset_index(drop=True, inplace=True)
    df_task = df_task[['req_time', 'start_node', 'end_node', 'move_time']]

    task_count = dict([(i, 0) for i in range(0, 24)])
    tasks = []
    for i, row in df_task.iterrows():
        task_count[int(row['req_time'][0:2])] += 1
        tasks.append((row['req_time'], row['start_node'], row['end_node']))

    # Vehicle Setting
    vehicle_mgr: VehicleManager = VehicleManager()

    vehicles_run_time = []
    vehicles_run_time.extend([0, 26] for _ in range(simulation_vehicle_num))

    # Schedule Setting
    schedule_mgr: ScheduleManager = ScheduleManager()

    print(f"Vehicle Num : {len(vehicles_run_time)}")
    for i in range(len(vehicles_run_time)):
        v_name = "V" + str(i)
        vehicle_mgr.add_vehicle(v_name, nodes[3878][0], nodes[3878][1])
        schedule_mgr.init_schedule(v_name)

    task_mgr: TaskManager = TaskManager()

    logs = []
    schedule_logs = []
    n_time: datetime = datetime.strptime("2023-02-02", '%Y-%m-%d')
    for h in range(0, simulation_time):
        print(f"============ Simulation Time : {h} hour processing.. task count : {task_count[h]}============")
        # update_weight(graph_name, h % 24 + 1)
        update_weight(graph_name, 1)

        for i, run_time in enumerate(vehicles_run_time):
            if run_time[0] == h:
                vehicle_mgr.open_vehicle("V" + str(i), n_time + timedelta(hours=run_time[1] - run_time[0]))
            if run_time[1] == h:
                vehicle_mgr.close_vehicle("V" + str(i))

        for m in range(60):
            n_time += timedelta(minutes=1)

            log, schedule_log = main_process_schedule(n_time, graph_name, vehicle_mgr, task_mgr, schedule_mgr, tasks, schedule_type, simulation_reschedule_time)
            logs.append(log)
            if len(schedule_log) > 0:
                schedule_logs.append(schedule_log)

            # logs.append(main_process(n_time, graph_name, vehicle_mgr, task_mgr, tasks))
    prev_schedule_logs = dict()

    for v_name in schedule_mgr.schedule_lists:
        schedule_list = schedule_mgr.get_schedule_list(v_name)

        for schedule in schedule_list.get_schedule_list_all():
            prev_schedule_logs[schedule.task_id] = schedule.get_log()

    sorted_prev_schedule_logs = sorted(prev_schedule_logs.items(), key=lambda x: x[0])

    print("============ Simulation End ============")
    print(f"Processing Time : {round(time.time() - start_time)}")

    json_obj = {'logs': logs,
                'schedules': schedule_logs,
                'prev_schedules': [value for key, value in sorted_prev_schedule_logs]}

    with open(f'log/{request_date}_{simulation_vehicle_num}_{simulation_task_num}.json', 'w') as outfile:
        json.dump(json_obj, outfile, indent=4)


if __name__ == "__main__":
    run()
