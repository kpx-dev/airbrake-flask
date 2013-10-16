"""
This is a very bad Flask app, always raise Exception
"""
from flask import Flask, request, got_request_exception
import gevent
from airbrake import AirbrakeErrorHandler
import sys

app = Flask(__name__)
EXCEPTION_MESSAGE = "bad_exception!"


@app.route('/')
def root():
    print "inside root /"
    raise Exception(EXCEPTION_MESSAGE)

    return 'this never return ok'


def log_exception(sender, exception, **extra):
    print "inside log_exception"
    handler = AirbrakeErrorHandler(api_key="AIRBRAKE_KEY_1234",
                                   env_name='test',
                                   request=request)
    # handler.emit(exception=exception, exc_info=sys.exc_info())
    gevent.spawn(handler.emit, exception, sys.exc_info())


got_request_exception.connect(log_exception, app)
