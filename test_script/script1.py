from datetime import datetime

from object.Vehicle import Vehicle
from object.Task import Task
from object.Location import Location
from object.VehicleMgr import VehicleMgr
from object.TaskMgr import TaskMgr

from allocator.vehicle_allocator import allocate

vehicle_mgr = VehicleMgr()
task_mgr = TaskMgr()

vehicle_mgr.add_vehicle("V1")
task_mgr.add_task(0, Location(10, 10), datetime.now(), 10)

allocate(vehicle_mgr, task_mgr, "V1", 0)
