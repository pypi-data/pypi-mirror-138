# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yarender']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'click>=8.0.3,<9.0.0', 'rich>=11.2.0,<12.0.0']

entry_points = \
{'console_scripts': ['yarender = yarender.main:render']}

setup_kwargs = {
    'name': 'yarender',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'DeDA',
    'author_email': 'denis.deryabin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
