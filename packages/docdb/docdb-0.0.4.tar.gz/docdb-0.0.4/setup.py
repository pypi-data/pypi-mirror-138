# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docdb']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.3,<2.0.0', 'pytest-cov>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'docdb',
    'version': '0.0.4',
    'description': 'A lightweight, performant, document database built on SQLite for Python3',
    'long_description': None,
    'author': 'Dan Sikes',
    'author_email': 'dansikes7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
