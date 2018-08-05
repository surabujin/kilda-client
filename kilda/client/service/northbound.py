# service.northbound

import requests

from kilda.client import endpoint

from . import abstract


class Northbound(abstract.AbstractService):
    def __init__(self, location):
        super().__init__(location)

        self.flow = FlowGroup(self, 'flows')


class FlowGroup(endpoint.AbstractGroup):
    def __init__(self, service, prefix):
        super().__init__(service, prefix)

        self.create = FlowsCreate(self, self.url)
        self.list = FlowsList(service, self.url)


class FlowsCreate(endpoint.AbstractEndpoint):
    def __call__(self, payload):
        return self.http_call(requests.Request('POST', self.url(), json=payload))


class FlowsList(endpoint.AbstractEndpoint):
    def __call__(self):
        return self.http_call(requests.Request('GET', self.url()))
