from Vehicle import Vehicle


class VehicleMgr:
    def __init__(self):
        self.vehicles: dict[str, Vehicle] = dict()
