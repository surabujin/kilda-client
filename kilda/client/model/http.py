# model.http

import uuid

import requests

from . import abstract


class RequestResponseBase(abstract.Abstract):
    identity = abstract.Default(uuid.uuid1, produce=True)

    def _sort_key(self):
        return (self.identity,)


class HTTPRequest(RequestResponseBase):
    request = abstract.Default(None)

    def __init__(self, request, **fields):
        super().__init__(request=request, **fields)


class HTTPResponse(RequestResponseBase):
    response = abstract.Default(None)
    error = abstract.Default(None)

    def __init__(self, identity, **fields):
        try:
            error = fields['error']
        except KeyError:
            pass
        else:
            if isinstance(error, requests.HTTPError):
                fields.setdefault('response', error.response)

        super().__init__(identity=identity, **fields)
