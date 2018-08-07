# service.northbound

from kilda.client.service import abstract
from .flow import Group


class Northbound(abstract.AbstractService):
    def __init__(self, location):
        super().__init__(location)

        self.flow = Group(self, 'flows')
