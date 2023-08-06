# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['testinghelloworld']
setup_kwargs = {
    'name': 'testinghelloworld',
    'version': '1.0.0',
    'description': 'no',
    'long_description': None,
    'author': 'Vitlie',
    'author_email': 'dercaci200@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
