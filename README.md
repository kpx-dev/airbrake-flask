airbrake-flask
==============

Airbrake client for Python Flask Microframework

License
-------
Licensed under the MIT License.

Example Usage with gevent
-------------------------
		from flask import Flask, request
		from airbrake import AirbrakeErrorHandler

		@app.errorhandler(500)
		def internal_error(error):
    	if app.config['EXCEPTION_LOGGING']:
			handler = AirbrakeErrorHandler(api_key=app.config['AIRBREAK_API_KEY'],
										   env_name=ENV,
										   request_url=request.url,
										   request_path=request.path,
										   request_method=request.method,
										   request_args=request.args,
										   request_headers=request.headers)
			gevent.spawn(handler.emit, error)