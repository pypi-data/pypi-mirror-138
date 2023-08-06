# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marathon_matches_manager']

package_data = \
{'': ['*'], 'marathon_matches_manager': ['static/*', 'templates/*']}

install_requires = \
['Flask>=2.0.3,<3.0.0', 'docopt>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['m3 = marathon_matches_manager.m3:main']}

setup_kwargs = {
    'name': 'marathon-matches-manager',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'kryInit',
    'author_email': 'kryinit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
