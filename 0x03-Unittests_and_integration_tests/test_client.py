#!/usr/bin/env python3
'''Parameterize and patch as decorators
   Farmialize with client.GitHubOrgClient.
'''
import unittest
from unittest.mock import Mock, patch, PropertyMock
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

    def test_public_repos_url(self):
        '''test public repo url'''
        payload = {'repose_url': 'https://api.github.com/orgs/testorg/repos'}
        with patch.object(
            GithubOrgClient, 'org', calla_ble=PropertyMock
        ) as org_mock:
            org_mock.return_value = payload
            user = GithubOrgClient('testorg')
            results = 'https://api.github.com/orgs/testorg/repos'
            self.assertEqual(user._public_repos_url, results)

    def test_public_repos(self, get_json):
        '''test public repo'''
        payload = [{'name': 'repos'}, {'name': 'repo'}]
        get_json.return_value = payload
        with patch.object(
            GithubOrgClient, '_public_repos_url', callable=PropertyMock
        ) as pub_url_repo_mock:
            pub_url_repo_mock.return_value = \
              'https://api.github.com/orgs/testorg/repos'
            user = GithubOrgClient('testorg')
            results = user.public_repos()
            self.assertEqual(results, ['repos', 'repo'])
            get_json.assert_called_once_with(
                'https://api.github.com/orgs/testorg/repos'
            )
