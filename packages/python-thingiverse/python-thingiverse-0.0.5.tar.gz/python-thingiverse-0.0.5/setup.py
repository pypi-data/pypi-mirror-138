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
    'version': '0.0.5',
    'description': 'A Python Thingiverse REST API wrapper',
    'long_description': '# Python Thingiverse\n\nNOT OFFICIAL. This is only a Python wrapper for Thingiverse REST API.\n\nThis project was started in Feb 10 2022. It is still being developed and improved. To see the Test PyPI package, check it [here](https://test.pypi.org/project/python-thingiverse/)\n\n## Table of Contents\n\n+ [Getting Started](#getting-started)\n  + [Usage](#usage)\n+ [Installing development package](#installing-development-package)\n+ [TODO](#todo)\n+ [Improvements](#improvements)\n\n\n### Getting Started\n\nTo install the package run\n\n```bash\npip install python-thingiverse\n```\n\n\n#### Usage\n\nInitializing the Thingiverse\n\n```python\nfrom thingiverse import Thingiverse\n\nthingy = Thingiverse(access_token="<access token>")\nsearch_results = thingy.search_term("RPi 4")\n```\n\n\n### Installing development package\n\n```bash\npython3 -m pip install -i https://test.pypi.org/simple/ python-thingiverse\n```\n\n\n### TODO:\n\n- A full list of REST endpoints will go here\n\n### Improvements\n\n- [X] Docstrings\n- [ ] OAuth working (Use App token!!!)\n- [X] CI/CD\n- [ ] Look into autoversioning\n- [X] Tests (started)\n- [ ] README\n- [ ] Think of documentation hosting\n',
    'author': 'Jose Garcia',
    'author_email': 'maton.pg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://garciajg.github.io/python-thingiverse/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
