airbrake-flask
==============

Airbrake client for Python Flask Microframework

[![Build Status](https://travis-ci.org/kienpham2000/airbrake-flask.png?branch=master)](https://travis-ci.org/kienpham2000/airbrake-flask)

License
-------
Licensed under the MIT License.

Testing / Coverage
------------------
To run tests, you need to install some required packages. Remember to activate your virtualenv first. 

	# install required packages for test
	$ pip install -e .[test]
	
	# run test
	$ nosetests
	
	# generate coverage report
	$ nosetests --with-coverage --cover-html
	

Example Usage with gevent
-------------------------
	from flask import Flask, request, got_request_exception
	from airbrake import AirbrakeErrorHandler
	import gevent
	import sys
		
	app = Flask(__name__)
	ENV = ('ENV' in os.environ and os.environ['ENV']) or 'prod'

	def log_exception(error):
		handler = AirbrakeErrorHandler(api_key="PUT_YOUR_AIRBRAKE_KEY_HERE",
										env_name=ENV,
										request=request)
		gevent.spawn(handler.emit, error, sys.exc_info())

    got_request_exception.connect(log_exception, app)
