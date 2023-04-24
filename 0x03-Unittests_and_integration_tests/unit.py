#!/usr/bin/env python3

import unittest
import string

def add(a, b):
    return a + b

def str_test():
    message = ''
    return message

class TestAdd(unittest.TestCase):

    def test_add(self):
        test = add(5, 5)
        self.assertEqual(test, 10)

    def test_is_str(self):
        result = str_test()
        self.assertIsInstance(result, str)

    def test_isstring(self):
        message = string.ascii_letters
        print(message)
if __name__ == "__main__":
    unittest.main()


