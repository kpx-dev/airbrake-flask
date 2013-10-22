import unittest
from tests import BaseTestCase
from bad_app import EXCEPTION_MESSAGE
from nose.tools import assert_equals


class IntegrationTests(BaseTestCase):
    def test_exception(self):
        try:
            res = self.app.get('/')
        except Exception, e:
            assert_equals(e.message, EXCEPTION_MESSAGE)

if __name__ == '__main__':
    unittest.main()
