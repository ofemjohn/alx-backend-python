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


@parameterized_class(
    ("org_payload", "payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''integration test'''

    @classmethod
    def setUpClass(cls):
        '''set up class'''
        setup = {'return_value.json.side_effect':
                 [
                     cls.org_payload, cls.payload,
                     cls.org_payload, cls.payload
                 ]
                 }
        cls.get_patcher = patch('requests.get', **setup)

        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        '''integration test'''
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        '''integration test'''
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        '''tear down'''
        cls.get_patcher.stop()
