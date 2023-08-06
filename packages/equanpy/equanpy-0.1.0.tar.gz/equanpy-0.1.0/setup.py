# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['equanpy']
setup_kwargs = {
    'name': 'equanpy',
    'version': '0.1.0',
    'description': 'Python packaging data school',
    'long_description': None,
    'author': 'Didier SCHMITT',
    'author_email': 'dschmitt@equancy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
