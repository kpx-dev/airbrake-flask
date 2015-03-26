import unittest
from tests import (BaseTestCase, API_KEY, API_URL, ENV_NAME, ENV_VAR, META_VAR,
                   TIMEOUT)
from nose.tools import assert_equals, assert_is_not_none
import xml.etree.ElementTree as ET


class UnitTests(BaseTestCase):
    def test_init(self):
        # make sure all vars are set from init
        assert_equals(self.client.api_key, API_KEY)
        assert_equals(self.client.api_url, API_URL)
        assert_equals(self.client.env_name, ENV_NAME)
        assert_equals(self.client.env_variables, ENV_VAR)
        assert_equals(self.client.meta_variables, META_VAR)
        assert_equals(self.client.timeout, TIMEOUT)

        # check Flask request object info:
        assert_is_not_none(self.client.request)
        assert_is_not_none(self.client.request['json'])

    def test_generate_xml(self):
        xml = self.client._generate_xml(exception=Exception('hola exception'))

        root = ET.fromstring(xml)
        payload = {
            root.tag: root.attrib,
        }

        for child in root:
            payload[child.tag] = child.attrib

        assert_equals(payload['notice'], {'version': '2.0'})
        assert_is_not_none(payload['server-environment'])
        assert_is_not_none(payload['request'])
        assert_is_not_none(payload['api-key'])
        assert_is_not_none(payload['error'])
        assert_is_not_none(payload['notifier'])

    def test_emit(self):
        code, message = self.client.emit(exception=Exception('hola exception'))
        assert_equals(code, 200)
        assert_is_not_none(message)

if __name__ == '__main__':
    unittest.main()
