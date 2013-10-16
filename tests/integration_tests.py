import unittest
import mock
from tests import BaseTestCase
from bad_app import EXCEPTION_MESSAGE


class IntegrationTests(BaseTestCase):
    @mock.patch('tests.bad_app.root')
    def test_exception(self, mocked):
        mocked.side_effect = Exception()

        try:
            res = self.app.get('/')
        except Exception, e:
            assert e.message == EXCEPTION_MESSAGE


if __name__ == '__main__':
    unittest.main()
