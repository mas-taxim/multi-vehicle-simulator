import os
import json
from datetime import datetime, timedelta
import logging


"""_summary_
log struct that this file using
{
    time : timestamp
    vehicles : [
        {
            name : vehicles name
            status : vehicle status
        }
        ...
    ]
    tasks : [
        {
            id : task id
            status : task status same as vehicles status
        }
    ]
}
"""

WAIT: int = 0
ALLOC: int = 1
MOVE_TO_LOAD: int = 2
LOAD_START: int = 3
LOADING: int = 4
LOAD_END: int = 5
MOVE_TO_UNLOAD: int = 6
UNLOAD_START: int = 7
UNLOADING: int = 8
UNLOAD_END: int = 9


vehicle_list = dict()
task_list = dict()


def init_sys_log():
    logFileName = datetime.now().strftime("%Y%m%d_%H%M%S") + "_statistics.log"

    sys_logger = logging.getLogger("statistics")
    sys_logger.setLevel(logging.INFO)

    # log 출력
    sys_log_handler = logging.FileHandler(f'sys_log/{logFileName}')
    sys_log_handler.setFormatter(
        logging.Formatter('%(levelname)s - %(message)s'))
    sys_logger.addHandler(sys_log_handler)


def read_log(log_path):
    with open(log_path, 'r') as file:
        logs = json.load(file)

    return logs['logs']


def get_latest_log(files_path: str) -> str:
    """_summary_
    get latest log file with log dir path
    Args:
        files_path (str): log file Path

    Returns:
        str: latest json log file
    """
    f_list = []
    for f_name in os.listdir(f"{files_path}"):
        if f_name == ".gitignore":
            continue
        written_time = os.path.getctime(f"{files_path}/{f_name}")
        f_list.append((f_name, written_time))

    # file list sort & get latest log file name
    latest_filename = sorted(f_list, key=lambda x: x[1], reverse=True)[0][0]

    return read_log(f"{files_path}/{latest_filename}")


def init_vehicle_list(logs: dict) -> None:
    """_summary_
    read log file and then make vehicle list
    Args:
        logs (dict): log(type : dict)
    """
    sys_logger = logging.getLogger("statistics")
    start_time = logs[0]['time']
    for vehicle in logs[0]['vehicles']:
        
        
        print(vehicle['name'])
        vehicle_list[vehicle['name']] = {
            'status': vehicle['status'], 'empty_time': 0, 'last_update_time': start_time}
    sys_logger.info(str(vehicle_list))


def add_task(tid: int, init_status: int, add_time: int) -> None:
    """_summary_
    add to tasklist
    Args:
        tid (int): task id
        init_status (int): task first status
        add_time (int): task added time
    """
    task_list[tid] = {'status': init_status, 'wait_alloc_time': 0,
                      'wait_vehicle_time': 0, 'last_update_time': add_time}


def run(logs: dict):

    sys_logger = logging.getLogger("statistics")

    # 1. vehicle list 생성
    init_vehicle_list(logs)

    cur_time: int
    # 2. looping in timestamp
    for log in logs:
        cur_time = log['time']
         
        # 2.1 task checking
        for task in log['tasks']:
            tid = task['id']

            if tid not in task_list:
                add_task(tid, task['status'], cur_time)

            if task['status'] > LOAD_START:
                continue
            elif task['status'] == WAIT:
                continue
            elif task['status'] == ALLOC:
                # before status check
                if task_list[tid]['status'] == ALLOC:
                    continue
                elif task_list[tid]['status'] > ALLOC:
                    sys_logger.error(
                        f"[task][ALLOC] task status is not correct -> time:{cur_time} / tid:{tid}")
                    continue

                # update data
                task_wait_start_time = task_list[tid]['last_update_time']
                task_list[tid]['wait_alloc_time'] = cur_time - \
                    task_wait_start_time
                task_list[tid]['last_update_time'] = cur_time
                task_list[tid]['status'] = ALLOC
                
            elif task['status'] == LOAD_START:
                # before status check
                if task_list[tid]['status'] == LOAD_START:
                    continue
                elif task_list[tid]['status'] > LOAD_START:
                    sys_logger.error(
                        f"[task][LOAD_START] task status is not correct -> time:{cur_time} / tid:{tid}")
                    continue
                
                # update data
                task_alloc_start_time = task_list[tid]['last_update_time']
                task_list[tid]['wait_vehicle_time'] = cur_time - \
                    task_alloc_start_time
                task_list[tid]['last_update_time'] = cur_time
                task_list[tid]['status'] = LOAD_START
                
        # TODO : 2.2 vehicle Checking




if __name__ == "__main__":

    #cur_dir = os.getcwd()
    log_dir = "./log"
    logs = get_latest_log(log_dir)

    init_sys_log()
    run(logs)
    
    for tid in task_list:
        print(f"tid : {tid}, data : {str(task_list[tid])}")
    