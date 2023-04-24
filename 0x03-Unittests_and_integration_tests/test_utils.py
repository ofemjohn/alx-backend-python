#!/usr/bin/env python3
'''python unittest module'''
import unittest
from parameterized import parameterized
import utils


class TestAccessNestedMap(unittest.TestCase):
    '''test nested maps with different keys and values'''
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, nested_map, path, expected_outcome):
        '''test the nested map with the path'''
        self.assertEqual(utils.access_nested_map(nested_map, path),
                         expected_outcome)
