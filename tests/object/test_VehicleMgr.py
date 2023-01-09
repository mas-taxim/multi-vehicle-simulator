import pytest
from datetime import datetime

from object.Location import Location
from object.VehicleMgr import Vehicle
from object.VehicleMgr import VehicleMgr


def test_script1():
    vehicle_mgr = VehicleMgr()
    vehicle_mgr.add_vehicle("V1")

    assert vehicle_mgr.get_vehicle("V1").name == "V1"
    assert vehicle_mgr.get_vehicle("V1").loc.x == 0
    assert vehicle_mgr.get_vehicle("V1").loc.y == 0
    assert vehicle_mgr.get_vehicle("V1").battery == 1
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.WAIT
    assert vehicle_mgr.get_vehicle("V1").dest is None
    assert vehicle_mgr.get_vehicle("V1").route == []

    assert len(vehicle_mgr.vehicles) == 1

