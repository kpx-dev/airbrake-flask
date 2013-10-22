import logging
import traceback
import requests
import os
import sys
from xml.etree.ElementTree import Element, tostring, SubElement
from . import __app_name__, __version__, __app_url__

_API_URL = 'https://airbrake.io/notifier_api/v2/notices'
_DEFAULT_ENV_VARIABLES = ['PATH', 'USER', 'HOME']
_DEFAULT_META_VARIABLES = ['HTTP_USER_AGENT', 'HTTP_COOKIE', 'REMOTE_ADDR',
                           'SERVER_NAME', 'SERVER_SOFTWARE']


class AirbrakeErrorHandler(logging.Handler):
    def __init__(self, api_key, env_name, request, api_url=_API_URL,
                 timeout=30, env_variables=_DEFAULT_ENV_VARIABLES,
                 meta_variables=_DEFAULT_META_VARIABLES, session=None,
                 root_path=None):
        logging.Handler.__init__(self)
        self.api_key = api_key
        self.api_url = api_url
        self.env_name = env_name
        self.env_variables = env_variables
        self.meta_variables = meta_variables
        self.timeout = timeout
        self.session = session
        self.root_path = root_path

        if self.root_path is None:
            self.root_path = os.path.dirname(os.path.abspath(__file__))

        # handle Flask request object:
        self.request = {
            'url': request.url,
            'path': request.path,
            'method': request.method,
            'values': request.values,
            'json': request.json,
            'headers': request.headers,
            'remote_addr': request.remote_addr
        }

    def emit(self, exception, exc_info=None):
        headers = {"Content-Type": "text/xml"}
        data = self._generate_xml(exception=exception, exc_info=exc_info)

        status = requests.post(url=self.api_url, headers=headers, data=data)

        return (status.status_code, status.text)

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
        SubElement(server_env, 'project-root').text = self.root_path

        request_xml = SubElement(xml, 'request')
        SubElement(request_xml, 'url').text = self.request['url']

        if self.request['path']:
            SubElement(request_xml, 'component').text = self.request['path']
            SubElement(request_xml, 'action').text = self.request['method']

        # check for session:
        if self.session:
            request_session = SubElement(request_xml, 'params')
            for key in self.session:
                SubElement(request_session, 'var', dict(key=key)).text = (str(
                    self.session[key]))

        # check for form, args or json data
        params = SubElement(request_xml, 'params')
        if self.request['values']:
            for key in self.request['values']:
                SubElement(params, 'var', dict(key=key)).text = (str(
                    self.request['values'].get(key)))

        if self.request['json']:
            for key in self.request['json']:
                SubElement(params, 'var', dict(key=key)).text = (str(
                    self.request['json'].get(key)))

        # TODO: add self.meta_variables here, learn how to extract from Flask
        cgi_data = SubElement(request_xml, 'cgi-data')
        for key, value in os.environ.items():
            if key in self.env_variables:
                SubElement(cgi_data, 'var', dict(key=key)).text = str(value)
        if self.request['remote_addr']:
            SubElement(cgi_data, 'var', dict(key='remote_addr')).text = str(
                self.request['remote_addr'])

        if self.request['headers']:
            for key, value in self.request['headers']:
                SubElement(cgi_data, 'var', dict(key=key)).text = str(value)

        # setting class name
        error = SubElement(xml, 'error')
        SubElement(error, 'class').text = exception.__class__.__name__
        SubElement(error, 'message').text = str(exception)

        # setting backtrace line
        backtrace = SubElement(error, 'backtrace')
        if trace is not None:
            for (pathname, lineno, func_name,
                 text) in traceback.extract_tb(trace)[::-1]:
                SubElement(backtrace, 'line', dict(file=pathname,
                                                   number=str(lineno),
                                                   method='%s: %s' % (func_name,
                                                                      text)))

        return tostring(xml)
