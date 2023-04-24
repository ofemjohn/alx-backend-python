#!/usr/bin/env python3
'''python unittest module'''
import unittest
from parameterized import parameterized
import utils
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    '''test nested maps with different keys and values'''
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, nested_map, path, expected_output):
        '''test the nested map with the path'''
        self.assertEqual(utils.access_nested_map(nested_map, path),
                         expected_output)

    @parameterized.expand([
        ({}, ('a',)),
        ({'a': 1}, ({'a', 'b'}))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        '''test map with exception thrown'''
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    '''test json'''
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_payload, test_url, get_json_mock):
        '''mock request'''
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        get_json_mock.return_value = mock_response

        results = utils.get_json(test_url)
        self.assertEqual(results, test_payload)
        get_json_mock.assert_called_once_with(test_url)
