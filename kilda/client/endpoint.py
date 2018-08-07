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

        request = http.prepare_request(request)
        request = model.HTTPRequest(request)

        self.http_events.send(self, request=request)
        try:
            response = http.send(request.request)
            self.http_events.send(request.identity, response=model.HTTPResponse(request.identity, response=response))
        except Exception as e:
            self.http_events.send(request.identity, error=e)
            raise

        response.raise_for_status()
        return response


class AbstractGroup(object):
    def __init__(self, service, prefix):
        self.service = service
        self.url = url.URLChain(service.url, prefix)
