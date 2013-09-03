import logging
import traceback
import urllib2
import os
import sys
from xml.etree.ElementTree import Element, tostring, SubElement

_API_URL = 'https://airbrake.io/notifier_api/v2/notices'
_DEFAULT_ENV_VARIABLES = []
_DEFAULT_META_VARIABLES = ['HTTP_USER_AGENT', 'HTTP_COOKIE', 'REMOTE_ADDR',
                           'SERVER_NAME', 'SERVER_SOFTWARE']
__app_name__ = 'flask_airbrake'
__version__ = '0.0.3'
__app_url__ = 'https://github.com/kienpham2000/airbrake-flask'


class AirbrakeErrorHandler(logging.Handler):
    def __init__(self, api_key, env_name, api_url=_API_URL,
                 timeout=30, env_variables=_DEFAULT_ENV_VARIABLES,
                 meta_variables=_DEFAULT_META_VARIABLES, request_url=None,
                 request_path=None, request_method=None, request_args=None,
                 request_headers=None):
        logging.Handler.__init__(self)
        self.api_key = api_key
        self.api_url = api_url
        self.env_name = env_name
        self.env_variables = env_variables
        self.meta_variables = meta_variables
        self.timeout = timeout
        self.request_url = request_url
        self.request_path = request_path
        self.request_method = request_method
        self.request_args = request_args
        self.request_headers = request_headers

    def emit(self, exception, exc_info=None):
        self._send_message(self._generate_xml(exception=exception,
                                              exc_info=exc_info))

    def _generate_xml(self, exception, exc_info=None):
        # pass in exc_info for traceback to work with gevent:
        _, _, trace = exc_info or sys.exc_info()

        xml = Element('notice', dict(version='2.0'))
        SubElement(xml, 'api-key').text = self.api_key

        notifier = SubElement(xml, 'notifier')
        SubElement(notifier, 'name').text = __app_name__
        SubElement(notifier, 'version').text = __version__
        SubElement(notifier, 'url').text = __app_url__

        server_env = SubElement(xml, 'server-environment')
        SubElement(server_env, 'environment-name').text = self.env_name

        request_xml = SubElement(xml, 'request')
        SubElement(request_xml, 'url').text = self.request_url

        if self.request_path:
            SubElement(request_xml, 'component').text = self.request_path
            SubElement(request_xml, 'action').text = self.request_method

        if self.request_args:
            params = SubElement(request_xml, 'params')
            for key in self.request_args:
                SubElement(params, 'var', dict(key=key)).text = \
                    str(self.request_args.get(key))

        cgi_data = SubElement(request_xml, 'cgi-data')
        for key, value in os.environ.items():
            if key in self.env_variables:
                SubElement(cgi_data, 'var', dict(key=key)).text = str(value)

        if self.request_headers:
            for key, value in self.request_headers:
                SubElement(cgi_data, 'var', dict(key=key)).text = str(value)

        error = SubElement(xml, 'error')
        SubElement(error, 'class').text = exception.__class__.__name__ if \
            exception else ''
        SubElement(error, 'message').text = str(exception)

        backtrace = SubElement(error, 'backtrace')
        if trace is not None:
            for (pathname, lineno, func_name,
                 text) in traceback.extract_tb(trace)[::-1]:
                SubElement(backtrace, 'line', dict(file=pathname,
                                                   number=str(lineno),
                                                   method='%s: %s' % (func_name,
                                                                      text)))

        return tostring(xml)

    def _send_http_request(self, headers, message):
        request = urllib2.Request(self.api_url, message, headers)
        try:
            response = urllib2.urlopen(request, timeout=self.timeout)
            status = response.getcode()
        except urllib2.HTTPError as e:
            status = e.code
        return status

    def _send_message(self, message):
        headers = {"Content-Type": "text/xml"}
        status = self._send_http_request(headers, message)
        if status == 200:
            return

        exception_message = "Unexpected status code {0}".format(str(status))

        if status == 403:
            exception_message = "Unable to send using SSL"
        elif status == 422:
            exception_message = "Invalid XML sent: {0}".format(message)
        elif status == 500:
            exception_message = ("Destination server is unavailable. "
                                 "Please check the remote server status.")
        elif status == 503:
            exception_message = ("Service unavailable. "
                                 "You may be over your quota.")

        return exception_message
