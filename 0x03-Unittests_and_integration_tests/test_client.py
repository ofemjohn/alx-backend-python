#!/usr/bin/env python3
'''Parameterize and patch as decorators
   Farmialize with client.GitHubOrgClient.
'''
import unittest
from unittest.mock import Mock, patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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
            url = 'https://api.github.com/orgs/testorg/repos'
            pub_url_repo_mock.return_value = url
            user = GithubOrgClient('testorg')
            results = user.public_repos()
            self.assertEqual(results, ['repos', 'repo'])
            get_json.assert_called_once_with(
                'https://api.github.com/orgs/testorg/repos'
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": {"key": "my_license", "name": "License name"}},
         "my_license", True),
        ({"license": {"key": "other_license", "name": "License name"}},
         "my_license", False),
    ])
    def test_has_license(self, repo, license_key, result):
        user = GithubOrgClient("testorg")
        self.assertEqual(user.has_license(repo, license_key), result)


@parameterized_class(['org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'], TEST_PAYLOAD)
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

    def test_public_repos(self):
        '''test public repo'''
        with patch.object(
            GithubOrgClient, '_public_repos_url', callable=PropertyMock
        ) as pub_url_repo_mock, patch('client.get_json') as get_json_mock:
            url = 'https://api.github.com/orgs/testorg/repos'
            pub_url_repo_mock.return_value = url
            get_json_mock.return_value = [{'name': 'repos'}, {'name': 'repo'}]
            user = GithubOrgClient('testorg')
            results = user.public_repos()
            self.assertEqual(results, ['repos', 'repo'])
            pub_url_repo_mock.assert_called_once_with(user)
            get_json_mock.assert_called_once_with(url)

    def test_public_repos_with_license(self):
        '''test public repo with license'''
        with patch.object(
            GithubOrgClient, '_public_repos_url', callable=PropertyMock
        ) as pub_url_repo_mock, patch('client.get_json') as get_json_mock:
            url = 'https://api.github.com/orgs/testorg/repos'
            pub_url_repo_mock.return_value = url
            get_json_mock.return_value = [
                {'name': 'repos', 'license': {'key': 'apache-2.0'}},
                {'name': 'repo', 'license': {'key': 'mit'}}
            ]
            user = GithubOrgClient('testorg')
            results = user.public_repos(license='apache-2.0')
            self.assertEqual(results, ['repos'])
            pub_url_repo_mock.assert_called_once_with(user)
            get_json_mock.assert_called_once_with(url)


if __name__ == "__main__":
    unittest.main()
