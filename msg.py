from typing import List


class HelperLatLon:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude


class Path:
    def __init__(self, waypoints: List[HelperLatLon]=[]):
        self.waypoints = waypoints
