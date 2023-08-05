# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_ansible
from pulpcore.client.pulp_ansible.models.ansible_git_remote import AnsibleGitRemote  # noqa: E501
from pulpcore.client.pulp_ansible.rest import ApiException

class TestAnsibleGitRemote(unittest.TestCase):
    """AnsibleGitRemote unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AnsibleGitRemote
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_ansible.models.ansible_git_remote.AnsibleGitRemote()  # noqa: E501
        if include_optional :
            return AnsibleGitRemote(
                proxy_url = '0', 
                sock_connect_timeout = 0.0, 
                password = '0', 
                tls_validation = True, 
                client_key = '0', 
                proxy_username = '0', 
                ca_cert = '0', 
                connect_timeout = 0.0, 
                rate_limit = 56, 
                max_retries = 56, 
                sock_read_timeout = 0.0, 
                download_concurrency = 1, 
                proxy_password = '0', 
                name = '0', 
                client_cert = '0', 
                pulp_labels = None, 
                url = '0', 
                total_timeout = 0.0, 
                headers = [
                    None
                    ], 
                username = '0', 
                metadata_only = True, 
                git_ref = '0'
            )
        else :
            return AnsibleGitRemote(
                name = '0',
                url = '0',
        )

    def testAnsibleGitRemote(self):
        """Test AnsibleGitRemote"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
