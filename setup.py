from setuptools import setup
from airbrake import __version__, __app_url__, __app_name__

setup(
    name=__app_name__,
    version=__version__,
    author='Kien Pham, Kane Kim',
    author_email='kien@sendgrid.com',
    url=__app_url__,
    license='LICENSE.txt',
    description='Airbrake client for Python Flask',
    long_description='Airbrake client for Python Flask',
    install_requires=['requests==2.0.0'],
    extras_require={
        'test': [
            'nose',
            'coverage',
            'mock',
            'blinker',
            'Flask',
            'gevent'
        ]
    },
    test_suite="tests"
)
