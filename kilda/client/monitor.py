# monitor

import blinker
import requests

import kilda.client


class Monitor(object):
    def __init__(self):
        signal = blinker.signal(kilda.client.signal_name('http-call'))
        signal.connect(self)

    def __call__(self, sender, **fields):
        for key, cls in (
                ('request', HTTPRequestHandler),
                ('response', HTTPResponseHandler)):
            try:
                payload = fields['key']
            except KeyError:
                continue
            h = cls(sender, payload)
            h()

        else:
            self.unhandled(sender, fields)

    def unhandled(self, sender, fields):
        print('There is no handler for signal from {!r} with fields {}'.format(
            sender, ', '.join(repr(x) for x in fields)))


class AbstractHandler(object):
    def __init__(self, monitor, sender, record):
        self.monitor = monitor
        self.sender = sender
        self.record = record

    def __call__(self):
        raise NotImplementedError


class HTTPRequestHandler(AbstractHandler):
    def __call__(self):
        request = self.record.request
        print('HTTP {} {}'.format(request.method, request.url), end='')
        if request.body:
            print(' payload {} bytes'.format(len(request.body)), end='')
        print()


class HTTPResponseHandler(AbstractHandler):
    def __call__(self):
        record = self.record
        print('HTTP >> ', end='')
        if record.response:
            self.report_response(record.response)
        elif record.error:
            self.report_error(record.error)
        else:
            print('unable to fetch response details')

    def report_response(self, response):
        print('code={}'.format(response.code), end='')
        print('time={}'.format(response.elapsed), end='')

        if not response.ok:
            print()
            for line in response.text.splitlines():
                print('>>> {}'.format(line))
        else:
            print()

    def report_error(self, error):
        print(error)
