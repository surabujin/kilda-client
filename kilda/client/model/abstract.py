# model.abstract

import json
import weakref


class Default(object):
    def __init__(self, value, produce=False, override_none=True):
        self._resolve_cache = weakref.WeakKeyDictionary()
        self.value = value
        self.produce = produce
        self.override_none = override_none

    def __get__(self, instance, owner):
        if instance is None:
            return self

        value = self.value
        if self.produce:
            value = value()

        setattr(instance, self._resolve_name(owner), value)
        return value

    def is_filled(self, instance):
        name = self._resolve_name(type(instance))
        data = vars(instance)
        return name in data

    def _resolve_name(self, owner):
        try:
            return self._resolve_cache[owner]
        except KeyError:
            pass

        for name in dir(owner):
            try:
                attr = getattr(owner, name)
            except AttributeError:
                continue
            if attr is not self:
                continue
            break
        else:
            raise RuntimeError(
                '{!r} Unable to resolve bounded name (UNREACHABLE)'.format(
                    self))

        self._resolve_cache[owner] = name
        return name


class Abstract(object):
    pack_exclude = frozenset()

    def __init__(self, **fields):
        cls = type(self)
        extra = set()
        for name in fields:
            extra.add(name)
            try:
                attr = getattr(cls, name)
            except AttributeError:
                continue
            if not isinstance(attr, Default):
                continue

            extra.remove(name)

            if attr.override_none and fields[name] is None:
                continue
            setattr(self, name, fields[name])

        if extra:
            raise TypeError('{!r} got unknown arguments: "{}"'.format(
                self, '", "'.join(sorted(extra))))

        self._verify_fields()

    def __str__(self):
        return '<{}:{}>'.format(
            type(self).__name__,
            json.dumps(self.pack(), sort_keys=True, cls=JSONEncoder))

    def __eq__(self, other):
        if not isinstance(other, Abstract):
            raise NotImplementedError
        return self._sort_key() == other._sort_key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def pack(self):
        fields = vars(self).copy()

        cls = type(self)
        for name in dir(cls):
            if name.startswith('_'):
                continue
            if name in fields:
                continue

            attr = getattr(cls, name)
            if not isinstance(attr, Default):
                continue
            fields[name] = getattr(self, name)

        for name in tuple(fields):
            if not name.startswith('_') and name not in self.pack_exclude:
                continue
            del fields[name]

        return fields

    def _verify_fields(self):
        pass

    def _sort_key(self):
        raise NotImplementedError

    @classmethod
    def _extract_fields(cls, data):
        data = data.copy()
        fields = {}
        for name in dir(cls):
            if name.startswith('_'):
                continue
            attr = getattr(cls, name)
            if not isinstance(attr, Default):
                continue

            try:
                fields[name] = data.pop(name)
            except KeyError:
                pass

        return fields, data


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Abstract):
            value = o.pack()
        else:
            value = super(JSONEncoder, self).default(o)
        return value
