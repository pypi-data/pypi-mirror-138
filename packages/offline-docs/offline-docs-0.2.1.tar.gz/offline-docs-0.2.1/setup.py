# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['offline_docs']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0',
 'typer>=0.4.0,<0.5.0',
 'urlpath>=1.2.0,<2.0.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['offline-docs = offline_docs.cli:main']}

setup_kwargs = {
    'name': 'offline-docs',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'top-on',
    'author_email': 'top-on@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
