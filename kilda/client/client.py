# client

from kilda.client import location
from kilda.client import monitor
from kilda.client import service


class Client(object):
    def __init__(self, location_map):
        self.location_map = location_map

        self.monitor = monitor.Monitor()
        self.nb = service.Northbound(location.LocationProxy(self, 'northbound'))
