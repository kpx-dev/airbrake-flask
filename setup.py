"""airbrake-flask - Airbrake client for Python Flask

airbrake-flask is a fast library that use the amazing requests library to send
error, exception messages to airbrake.io. You can use this library with the
amazing gevent library to send your request asynchronously.
"""

classifiers = """\
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python :: 2
Topic :: Software Development :: Quality Assurance
Topic :: Software Development :: Testing
Development Status :: 5 - Production/Stable
""".splitlines()

from setuptools import setup
from airbrake import __version__, __app_url__, __app_name__

doc = __doc__.splitlines()

setup(
    name=__app_name__,
    version=__version__,
    packages=['airbrake'],
    zip_safe=False,
    author='Kien Pham, Kane Kim',
    author_email='kien@sendgrid.com',
    url=__app_url__,
    license='MIT',
    description=doc[0],
    long_description='\n'.join(doc[2:]),
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
    test_suite="tests",
    keywords='error airbrake flask exception',
    classifiers=classifiers
)
