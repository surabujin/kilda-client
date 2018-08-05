# url

import urllib.parse


class AbstractUrl(object):
    def __call__(self, *path, **qs):
        raise NotImplementedError


class URL(AbstractUrl):
    def __init__(self, location):
        self.location = location

    def __call__(self, *path, **qs):
        path = self.make_path(path)
        qs = self.make_qs(qs)
        return self.make_url(path, qs)

    def make_url(self, path, qs):
        chunks = ('', '', path, '', qs, '')
        url = urllib.parse.urlunparse(chunks)
        return urllib.parse.urljoin(self.base(), url)

    def base(self):
        return self.location().base_url

    @staticmethod
    def make_path(path):
        return '/'.join(urllib.parse.quote(chunk, safe='') for chunk in path)

    @staticmethod
    def make_qs(qs):
        if not qs:
            return ''
        return urllib.parse.urlencode(qs)


class URLChain(AbstractUrl):
    def __init__(self, upper, path, *extra):
        self.upper = upper
        path = [path]
        path.extend(extra)
        self.path = tuple(path)

    def __call__(self, *path, **qs):
        return self.upper(*(self.path + path), **qs)
