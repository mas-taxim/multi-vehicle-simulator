from object.Vehicle import Vehicle
from object.VehicleManager import VehicleManager


def test_add_one_vehicle():
    vehicle_manager = VehicleManager()
    vehicle_manager.add_vehicle("V1", 0, 0)

    assert vehicle_manager.get_vehicle("V1").name == "V1"
    assert vehicle_manager.get_vehicle("V1").loc.x == 0
    assert vehicle_manager.get_vehicle("V1").loc.y == \
        0
    assert vehicle_manager.get_vehicle("V1").battery == 1
    assert vehicle_manager.get_vehicle("V1").status == Vehicle.WAIT
    assert vehicle_manager.get_vehicle("V1").route == []

    assert len(vehicle_manager.vehicles) == 1
