import unittest
from flask import request
from tests import (BaseTestCase, API_KEY, API_URL, ENV_NAME, ENV_VAR, META_VAR,
                   TIMEOUT)


class UnitTests(BaseTestCase):

    def test_init(self):
        # make sure all vars are set from init
        assert self.client.api_key == API_KEY
        assert self.client.api_url == API_URL
        assert self.client.env_name == ENV_NAME
        assert self.client.env_variables == ENV_VAR
        assert self.client.meta_variables == META_VAR
        assert self.client.timeout == TIMEOUT

        # check Flask request object info:
        assert self.client.request is not None

    def test_generate_xml(self):
        # xml = self.client._generate_xml(exception=Exception('hola'))
        # print xml
        pass

if __name__ == '__main__':
    unittest.main()
