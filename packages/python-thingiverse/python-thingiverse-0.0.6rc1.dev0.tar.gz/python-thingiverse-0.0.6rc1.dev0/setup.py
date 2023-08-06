# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thingiverse']

package_data = \
{'': ['*'], 'thingiverse': ['types/*']}

install_requires = \
['Mako==1.1.6',
 'Markdown==3.3.6',
 'MarkupSafe==2.0.1',
 'attrs==21.4.0',
 'certifi==2021.10.8',
 'charset-normalizer==2.0.11',
 'coverage==6.3.1',
 'distlib==0.3.4',
 'filelock==3.4.2',
 'idna==3.3',
 'iniconfig==1.1.1',
 'mypy-extensions==0.4.3',
 'mypy==0.931',
 'nose==1.3.7',
 'packaging==21.3',
 'pdoc3==0.10.0',
 'platformdirs==2.5.0',
 'pluggy==1.0.0',
 'py==1.11.0',
 'pyparsing==3.0.7',
 'pytest-cov==3.0.0',
 'pytest==7.0.0',
 'python-box==5.4.1',
 'python-dotenv==0.19.2',
 'requests==2.27.1',
 'six==1.16.0',
 'toml==0.10.2',
 'tomli==2.0.1',
 'tox==3.24.5',
 'types-requests==2.27.9',
 'types-urllib3==1.26.9',
 'typing-extensions==4.0.1',
 'urllib3==1.26.8',
 'virtualenv==20.13.1']

setup_kwargs = {
    'name': 'python-thingiverse',
    'version': '0.0.6rc1.dev0',
    'description': 'A Python Thingiverse REST API wrapper',
    'long_description': '# Python Thingiverse\n\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/garciajg/python-thingiverse.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/garciajg/python-thingiverse/alerts/)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/garciajg/python-thingiverse.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/garciajg/python-thingiverse/context:python)\n\n\nNOT OFFICIAL. This is only a Python wrapper for Thingiverse REST API.\n\nThis project was started in Feb 10 2022. It is still being developed and improved. To see the Test PyPI package, check it [here](https://test.pypi.org/project/python-thingiverse/).\n\nThis project uses [python-box](https://pypi.org/project/python-box/) enpoint response. Python Box allows for use of dot-notation in dictionaries, this includes making inaccessible keys safe to access as well.\n\n```python\n# From python-box documentation https://pypi.org/project/python-box/\nfrom box import Box\n\nmovie_box = Box({ "Robin Hood: Men in Tights": { "imdb stars": 6.7, "length": 104 } })\n\nmovie_box.Robin_Hood_Men_in_Tights.imdb_stars\n# 6.7\n```\n\nCheck out full (python-thingiverse documentation)[https://garciajg.github.io/python-thingiverse/]\n\n## Table of Contents\n\n+ [Getting Started](#getting-started)\n  + [Usage](#usage)\n+ [Installing development package](#installing-development-package)\n+ [TODO](#todo)\n+ [Improvements](#improvements)\n\n\n### Getting Started\n\nTo install the package run\n\n```bash\npip install python-thingiverse\n```\n\n\n#### Usage\n\nInitializing the Thingiverse\n\n```python\nfrom thingiverse import Thingiverse\n\nthingy = Thingiverse(access_token="<access token>")\nsearch_results = thingy.search_term("RPi 4")\n```\n\n\n### Installing development package\n\n```bash\npython3 -m pip install -i https://test.pypi.org/simple/ python-thingiverse\n```\n\n\n### TODO:\n\n- `PATCH /users/{$username}/`\n- `DELETE /users/{$username}/`\n\n\n### Improvements\n\n- [X] Docstrings\n- [X] OAuth working (Use App token!!!)\n- [X] CI/CD\n- [ ] Look into autoversioning\n- [X] Tests (started)\n- [X] README (in progress)\n- [X] Think of documentation hosting\n',
    'author': 'Jose Garcia',
    'author_email': 'maton.pg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://garciajg.github.io/python-thingiverse/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
