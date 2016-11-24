"""Setup script for clChecker."""
from __future__ import print_function
from setuptools import setup
import codecs
import os
import unittest


HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Return multiple read calls to different readable objects as a single
    string."""
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

LONG_DESCRIPTION = read('README.md')


setup(
    name='clchecker',
    version='1.0.0',
    url='https://github.com/LuisUrrutia/clchecker',
    license='MIT License',
    author='Luis Urrutia',
    author_email='luis@urrutia.me',
    description='Check if a domain is available in NIC Chile',
    long_description=LONG_DESCRIPTION,
    install_requires=[
        'requests>=2.12.1'
        ],
    packages=['clchecker'],
    platforms='any',
    test_suite='setup.my_test_suite',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Topic :: Internet',
        ],
)