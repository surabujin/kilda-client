# service map

from kilda.client import exc


class LocationMap(object):
    def __init__(self):
        self.map = {}

    def add(self, name, record):
        if name in self.map:
            raise exc.ServiceDefineError('Service {} already defined'.format(name))
        self.map[name] = record

    def __call__(self, name):
        try:
            record = self.map[name]
        except KeyError:
            raise exc.ServiceNotFoundError(name)
        return record


class Location(object):
    auth = tuple()

    def __init__(self, base_url, auth=None):
        self.base_url = base_url
        if auth:
            self.auth = auth


class LocationProxy(object):
    def __init__(self, client, name):
        self.client = client
        self.name = name

    def __call__(self):
        return self.client.location_map(self.name)
