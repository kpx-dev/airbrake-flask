from airbrake.airbrake import AirbrakeErrorHandler
import os
from flask.testing import FlaskClient
import unittest
import bad_app

API_KEY = "AIRBRAKE_UNIT_TEST_KEY"
API_URL = "http://example.com"
TIMEOUT = 40
ENV_NAME = "SOME_ENV_NAME"
ENV_VAR = "TEST"
META_VAR = "SOME_META"


class TestClient(FlaskClient):
    pass


class FakeRequest(object):
    url = None
    path = None
    method = None
    values = {"some_form_key": "some_form_value"}
    json = {"json_key": "json_value"}
    data = '{"json_key": "json_value"}'
    headers = None
    remote_addr = 'localhost'


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        bad_app.app.config['TESTING'] = True
        self.app = bad_app.app.test_client()

        fake_session = {'username': 'airbrake_user'}
        self.client = AirbrakeErrorHandler(
            api_key=API_KEY,
            api_url=API_URL,
            timeout=TIMEOUT,
            env_name=ENV_NAME,
            env_variables=ENV_VAR,
            meta_variables=META_VAR,
            request=FakeRequest,
            session=fake_session,
            root_path=os.path.dirname(os.path.abspath(__file__)),
        )

    def tearDown(self):
        pass
