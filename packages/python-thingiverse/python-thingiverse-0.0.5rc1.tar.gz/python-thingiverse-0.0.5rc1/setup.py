# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thingiverse']

package_data = \
{'': ['*'], 'thingiverse': ['types/*']}

install_requires = \
['pytest-cov>=3.0.0,<4.0.0',
 'pytest>=7.0.0,<8.0.0',
 'python-box>=5.4.1,<6.0.0',
 'requests>=2.27.1,<3.0.0',
 'tox>=3.24.5,<4.0.0']

setup_kwargs = {
    'name': 'python-thingiverse',
    'version': '0.0.5rc1',
    'description': 'A Python Thingiverse REST API wrapper',
    'long_description': None,
    'author': 'Jose Garcia',
    'author_email': 'maton.pg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
