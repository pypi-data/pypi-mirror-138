# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lbst']
setup_kwargs = {
    'name': 'lbst',
    'version': '0.0.0',
    'description': 'Immutable Log-Balanced Search Tree',
    'long_description': None,
    'author': 'Amirouche',
    'author_email': 'amirouche@hyper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
