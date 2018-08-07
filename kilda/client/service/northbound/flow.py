# service.northbound.flow

import requests

from kilda.client import endpoint


class Group(endpoint.AbstractGroup):
    def __init__(self, service, prefix):
        super().__init__(service, prefix)

        self.create = Create(self, self.url)
        self.list = List(service, self.url)
        self.status = Status(service, self.url)
        self.path = Path(service, self.url)


class Create(endpoint.AbstractEndpoint):
    def __call__(self, payload):
        return self.http_call(requests.Request('PUT', self.url(), json=payload))


class List(endpoint.AbstractEndpoint):
    def __call__(self):
        return self.http_call(requests.Request('GET', self.url()))


class Status(endpoint.AbstractEndpoint):
    def __call__(self, flow_id):
        return self.http_call(requests.Request('GET', self.url('status', flow_id)))


class Path(endpoint.AbstractEndpoint):
    def __call__(self, flow_id):
        return self.http_call(requests.Request('GET', self.url(flow_id, 'path')))
