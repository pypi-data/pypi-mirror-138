# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lbst']
setup_kwargs = {
    'name': 'lbst',
    'version': '0.0.1',
    'description': 'Immutable Log-Balanced Search Tree',
    'long_description': '# Immutable Log-Balanced Search Tree\n\n![pink sakura tree at daytime](https://images.unsplash.com/photo-1515863149848-223cbed59017?w=1024&q=80)\n',
    'author': 'Amirouche',
    'author_email': 'amirouche@hyper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
