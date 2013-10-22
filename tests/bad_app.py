"""
This is a very bad Flask app, always raise Exception
"""
import os
from gevent import monkey
monkey.patch_all()
from flask import Flask, request, got_request_exception, session
from airbrake import AirbrakeErrorHandler
import sys
import gevent


app = Flask(__name__)
EXCEPTION_MESSAGE = "bad_exception!"


@app.route('/', methods=['POST', 'GET'])
def root():
    raise Exception(EXCEPTION_MESSAGE)

    return 'this never return ok'


def log_exception(sender, exception, **extra):
    handler = AirbrakeErrorHandler(api_key="AIRBRAKE_KEY_HERE",
                                   env_name='test',
                                   request=request,
                                   session=session
                                   )

    gevent.spawn(handler.emit, exception, sys.exc_info())


got_request_exception.connect(log_exception, app)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
