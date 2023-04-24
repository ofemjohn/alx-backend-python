#!/usr/bin/env python3
'''Parameterize and patch as decorators
   Farmialize with client.GitHubOrgClient.
'''
import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ('google', {'payload': True}),
        ('abc', {'payload': False})
    ])
    @patch('client.get_json')
    def test_org(self, org_n, payload_expected, mock_response):
        mock_response.return_value = payload_expected
        user = GithubOrgClient(org_n)
        self.assertEqual(user.org, payload_expected)
        mock_response.assert_called_once_with(
            f"https://api.github.com/orgs/{org_n}"
        )
