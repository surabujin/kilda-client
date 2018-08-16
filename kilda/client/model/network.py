# -*- coding:utf-8 -*-

import re


class SwitchId(object):
    @classmethod
    def of(cls, raw):
        parsers = [cls]
        history = set()
        while parsers:
            p = parsers.pop(0)
            if p in history:
                continue
            history.add(p)

            parsers.extend(p.__subclasses__())

            try:
                value = p(raw)
            except (ValueError, TypeError) as e:
                continue

            break
        else:
            raise ValueError(
                'Unable to extract SwitchId value from {!r}'.format(raw))

        return value

    def __init__(self, value):
        if not isinstance(value, int):
            value = int(value, 0)
        if value < 0 or 0xffff_ffff_ffff_ffff < value:
            raise ValueError('SwitchId value 0x{:x} if out of range')

        self.internal = value

    def __eq__(self, other):
        if not isinstance(other, SwitchId):
            return NotImplemented
        return self.internal == other.internal

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'SW{:016X}'.format(self.internal)

    def as_floodlight(self):
        return self._colonseparated_bytes(self._as_hex_sequence())

    def as_mac_address(self):
        return self._colonseparated_bytes(self._as_hex_sequence()[4:])

    def _as_hex_sequence(self):
        return '{:016x}'.format(self.internal)

    def _colonseparated_bytes(self, hex_sequence):
        seq = hex_sequence[::-1]
        return (':'.join(
            seq[x:x + 2] for x in range(0, len(seq), 2)))[::-1]


class SwitchIdStringPattern(SwitchId):
    pattern = re.compile(r'^$')

    @classmethod
    def transform(cls, value):
        return value

    def __init__(self, value):
        if type(self) is SwitchIdStringPattern:
            raise TypeError('Deny abstract type creation')

        if not self.pattern.match(value):
            raise ValueError('does not match the pattern')
        super().__init__(self.transform(value))


class SwitchIdFloodlight(SwitchIdStringPattern):
    pattern = re.compile(r'^(?:[0-9a-f]{2}:){7}[0-9a-f]{2}$', re.IGNORECASE)

    @classmethod
    def transform(cls, value):
        return '0x' + value.replace(':', '', 7)


class SwitchIdMacAddress(SwitchIdStringPattern):
    pattern = re.compile(r'^(?:[0-9a-f]{2}:){5}[0-9a-f]{2}$', re.IGNORECASE)

    @classmethod
    def transform(cls, value):
        return '0x' + value.replace(':', 5)


class SwitchIdCommon(SwitchIdStringPattern):
    pattern = re.compile(r'^SW[0-9a-f]{16}$', re.IGNORECASE)

    @classmethod
    def transform(cls, value):
        return '0x' + value[2:]
