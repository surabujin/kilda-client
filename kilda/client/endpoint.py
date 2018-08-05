# endpoint

import blinker

import kilda.client
from kilda.client import model
from kilda.client import url


class AbstractEndpoint(object):
    http_events = blinker.signal(kilda.client.signal_name('http-call'))

    def __init__(self, service, url):
        self.service = service
        self.url = url

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def http_call(self, request):
        http = self.service.http

        prepared = http.prepare_request(request)
        prepared = model.HTTPRequest(prepared)

        self.http_events.send(self, request=prepared.request)
        try:
            response = http.send(prepared)
            response.raise_for_status()

            self.http_events.send(prepared.identity, response=model.HTTPResponse(prepared.identity, response=response))
        except Exception as e:
            self.http_events.send(prepared.identity, error=e)
            raise

        return response


class AbstractGroup(object):
    def __init__(self, service, prefix):
        self.service = service
        self.url = url.URLChain(service.url, prefix)
