airbrake-flask
==============

Airbrake client for Python Flask Microframework

[![Build Status](https://travis-ci.org/kienpham2000/airbrake-flask.png?branch=master)](https://travis-ci.org/kienpham2000/airbrake-flask) [![Coverage Status](https://coveralls.io/repos/kienpham2000/airbrake-flask/badge.png?branch=master)](https://coveralls.io/r/kienpham2000/airbrake-flask?branch=master)
[![Code Health](https://landscape.io/github/kienpham2000/airbrake-flask/master/landscape.svg?style=flat-square)](https://landscape.io/github/kienpham2000/airbrake-flask/master)
[![Downloads](https://pypip.in/d/airbrake-flask/badge.png)](https://crate.io/packages/airbrake-flask/) [![Version](https://pypip.in/v/airbrake-flask/badge.png)](https://crate.io/packages/airbrake-flask/)

License
-------
Licensed under the MIT License.

Testing / Coverage
------------------
To run tests, you need to install some required packages. Remember to activate your virtualenv first. 

	# install required packages for test
	$ pip install -e .[test]
	
	# run test
	$ make test
	
	# generate coverage report
	$ make cover
	

Example Usage with gevent
-------------------------
	from flask import Flask, request, got_request_exception
	from airbrake.airbrake import AirbrakeErrorHandler
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
