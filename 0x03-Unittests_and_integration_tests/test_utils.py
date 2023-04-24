#!/usr/bin/env python3
'''python unittest module'''
import unittest
from parameterized import parameterized
import utils
from unittest.mock import patch, Mock
from utils import memoize


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


class TestMemoize(unittest.TestCase):
    '''Test memoize method'''

    def test_memoize(self):
        '''Test memoize'''
        class TestClass:
            '''Test class'''

            def a_method(self):
                '''test method'''
                return 42

            @memoize
            def a_property(self):
                '''check memoization'''
                return self.a_method()
        with patch.object(TestClass, 'a_method') as mock_method:
            test_result_1 = TestClass()
            test_result_1.a_property
            test_result_1.a_property
            mock_method.assert_called_once()
