import sys, os
import json
import logging
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from entity import Task as t, Vehicle as v


"""
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


sys_logger = logging.getLogger("statistics")

vehicle_list = dict()
"""
key : vehicle name
status : vehicle status
wait_alloc_time : status 9 - status 1
moving_to_load_time : status 1 - status 3
empty_event : [[event_end_time, wait_alloc_time]]
"""
task_list = dict()


def init_sys_log(logLevel: int):
    logFileName = datetime.now().strftime("%Y%m%d_%H%M%S") + "_statistics.log"

    sys_logger.setLevel(logLevel)

    # log 출력
    sys_log_handler = logging.FileHandler(f'statistics/sys_log/{logFileName}')
    sys_log_handler.setFormatter(
        logging.Formatter('%(levelname)s - %(message)s'))
    sys_logger.addHandler(sys_log_handler)


def read_log(log_path):
    with open(log_path, 'r') as file:
        logs = json.load(file)

    return logs['logs']


def get_latest_log(files_path: str) -> str:
    """
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
    if len(f_list) == 0:
        return None
    latest_filename = sorted(f_list, key=lambda x: x[1], reverse=True)[0][0]
    sys_logger.info(f"Using logfile name : {latest_filename}")
    return read_log(f"{files_path}/{latest_filename}")


def init_vehicle_list(logs: dict) -> None:
    """
    read log file and then make vehicle list
    Args:
        logs (dict): log(type : dict)
    """
    start_time = logs[0]['time']
    sys_logger.info("INIT vehicle information")
    for vehicle in logs[0]['vehicles']:
        vehicle_list[vehicle['name']] = {
            'status': vehicle['status'], 'wait_alloc_time': 0, 'moving_to_load_time': 0, 'last_update_time': start_time, 'empty_event': []}
        sys_logger.info(f"vehicle name : {vehicle['name']}, value : {str(vehicle_list[vehicle['name']])}")


def add_task(tid: int, init_status: int, add_time: int) -> None:
    """
    add to tasklist
    Args:
        tid (int): task id
        init_status (int): task first status
        add_time (int): task added time
    """
    task_list[tid] = {'status': init_status, 'wait_alloc_time': 0,
                      'wait_vehicle_time': 0, 'last_update_time': add_time, 'create_time': add_time}


def task_processing(tid: int, status: int, cur_time: int):
    """
    each logging time, task log processing
    Args:
        tid (int): task id
        status (int): task status
        cur_time (int): logging time
    """
    
    if tid not in task_list:
        add_task(tid, status, cur_time)
    
    # Case 1 : STATUS WAIT -> ALLOC
    if status == t.MOVE_TO_LOAD and task_list[tid]['status'] < t.MOVE_TO_LOAD:
        task_list[tid]['wait_alloc_time'] = cur_time - \
            task_list[tid]['last_update_time']
        task_list[tid]['last_update_time'] = cur_time
    
    # Case 2 : STATUS ALLOC -> LOAD_START
    elif status == t.LOAD_START and task_list[tid]['status'] < t.LOAD_START:
        task_list[tid]['wait_vehicle_time'] = cur_time - \
            task_list[tid]['last_update_time']
        task_list[tid]['last_update_time'] = cur_time
    
    task_list[tid]['status'] = status


def vehicle_processing(vname: str, status: int, cur_time: int):
    """
    each logging time, vehicle log processing
    Args:
        vname (str): vehicle name
        status (int): vehicle status
        cur_time (int): logging time
    """
    
    # Case 1 : STATUS WAIT -> ALLOC -> MOVE_TO_LOAD
    if status == v.MOVE_TO_LOAD and vehicle_list[vname]['status'] < v.MOVE_TO_LOAD:
        vehicle_list[vname]['wait_alloc_time'] += cur_time - \
            vehicle_list[vname]['last_update_time']
        sys_logger.info(f"[{vname}][{cur_time}] : WAIT -> ALLOC, sub1 += {cur_time - vehicle_list[vname]['last_update_time']}")
        vehicle_list[vname]['empty_event'].append([vehicle_list[vname]['last_update_time'], cur_time - vehicle_list[vname]['last_update_time']])
        vehicle_list[vname]['last_update_time'] = cur_time
    
    # Case 2 : STATUS ALLOC -> LOAD_START
    elif status == v.LOAD_START and vehicle_list[vname]['status'] < v.LOAD_START:
        vehicle_list[vname]['moving_to_load_time'] += cur_time - \
            vehicle_list[vname]['last_update_time']
        sys_logger.info(f"[{vname}][{cur_time}] : ALLOC -> LOAD_START, sub2 += {cur_time - vehicle_list[vname]['last_update_time']}")
        vehicle_list[vname]['last_update_time'] = cur_time
    
    vehicle_list[vname]['status'] = status


def generate_result(logs: dict) -> dict:
    # 1. vehicle list 생성
    init_vehicle_list(logs)

    cur_time: int
    # 2. looping in timestamp
    for log in logs:
        cur_time = log['time']
         
        # 2.1 task checking
        for task in log['tasks']:
            task_processing(task['id'], task['status'], cur_time)

        # 2.2 vehicle Checking
        for vehicle in log['vehicles']:
            vehicle_processing(vehicle['name'], vehicle['status'], cur_time)
            
    # 3. write result
    result = {'task': task_list, 'vehicle': vehicle_list}

    #log_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'statistics/log/result.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)

    return result

if __name__ == "__main__":

    #cur_dir = os.getcwd()
    log_dir = "./log"
    init_sys_log(logging.INFO)
    logs = get_latest_log(log_dir)
    
    if logs == None:
        sys_logger.error("log is not exist.")
        exit()
    
    generate_result(logs)
    
    # logging INFO
    sys_logger.info("LAST task information")
    for tid in task_list:
        #print(f"tid : {tid}, data : {str(task_list[tid])}")
        sys_logger.info(f"tid : {tid}, data : {str(task_list[tid])}")
    
    for vname in vehicle_list:
        #print(f"tid : {tid}, data : {str(task_list[tid])}")
        sys_logger.info(f"vname : {vname}, data : {vehicle_list[vname]}")
    