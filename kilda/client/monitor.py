# monitor

import blinker

import kilda.client


class Monitor(object):
    def __init__(self):
        signal = blinker.signal(kilda.client.signal_name('http-call'))
        signal.connect(self)

    def __call__(self, sender, **fields):
        for key, cls in (
                ('request', HTTPRequestHandler),
                ('response', HTTPResponseHandler),
                ('error', HTTPErrorHandler)):
            try:
                payload = fields[key]
            except KeyError:
                continue

            h = cls(self, sender, payload)
            h()

            break

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
        print('HTTP >> ', end='')
        self.fetch_response()

    def fetch_response(self):
        record = self.record
        if record.response:
            self.out_response(record.response)
        else:
            print('unable to fetch response details')

    def out_response(self, response):
        print('code={}'.format(response.status_code), end=' ')
        print('time={}'.format(response.elapsed), end='')

        if not response.ok:
            print()
            for line in response.text.splitlines():
                print('>>> {}'.format(line))
        else:
            print()

    def report_error(self, error):
        print(error)


class HTTPErrorHandler(AbstractHandler):
    def __call__(self):
        print('HTTP error - {}'.format(self.record))
