# service.abstract

import requests
import requests.auth

from kilda.client import url


class AbstractService(object):
    def __init__(self, location):
        self.location = location

        self.url = url.URL(location)

        self.http = requests.Session()
        self.http.headers.update({
            'accept': 'application/json'
        })
        self.http.auth = AuthProxy(self.location)


class AuthProxy(requests.auth.AuthBase):
    def __init__(self, location):
        self.location = location

    def __call__(self, r):
        auth = self.location().auth
        if not auth:
            return r

        h = requests.auth.HTTPBasicAuth(*auth)
        return h(r)
