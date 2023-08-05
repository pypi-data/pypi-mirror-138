# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tartine']
setup_kwargs = {
    'name': 'tartine',
    'version': '0.2.0',
    'description': 'Create dynamic spreadsheets using Python',
    'long_description': None,
    'author': 'MaxHalford',
    'author_email': 'maxhalford25@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
