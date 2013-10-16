from airbrake import AirbrakeErrorHandler
import os
from flask import Flask, request, g
from flask.testing import FlaskClient
import unittest
import mock
import bad_app

API_KEY = "AIRBRAKE_UNIT_TEST_KEY"
API_URL = "http://test_api_url"
TIMEOUT = 40
ENV_NAME = "SOME_ENV_NAME"
ENV_VAR = "TEST"
META_VAR = "SOME_META"


class TestClient(FlaskClient):
    pass


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        bad_app.app.config['TESTING'] = True
        self.app = bad_app.app.test_client()
        self.client = AirbrakeErrorHandler(
            api_key=API_KEY,
            api_url=API_URL,
            timeout=TIMEOUT,
            env_name=ENV_NAME,
            env_variables=ENV_VAR,
            meta_variables=META_VAR,
            request=request
        )

    def tearDown(self):
        pass
