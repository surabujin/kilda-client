# -*- coding:utf-8 -*-

import unittest

from kilda.client import model


class TestNetworkModel(unittest.TestCase):
    def test_switch_id(self):
        for origin, expect in (
                ('ff:ff:00:00:01:02:03:04', 0xffff000001020304),
                ('FF:FF:00:00:01:02:03:04', 0xffff000001020304),
                ('SWFFFF000001020304', 0xffff000001020304),
                ('SWffff000001020304', 0xffff000001020304),
                (1, 0x1),):
            actual = model.SwitchId.of(origin)

            self.assertEqual(expect, actual.internal)

    def test_invalid_switch_id(self):
        for raw in (
                -1,
                0x1_ffff_0000_1122_3344,
                'ff:zf:00:00:01:02:03:04'):
            self.assertRaises(ValueError, model.SwitchId.of, raw)
