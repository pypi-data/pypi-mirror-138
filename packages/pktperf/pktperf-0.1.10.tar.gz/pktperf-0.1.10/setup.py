# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pktperf']

package_data = \
{'': ['*']}

install_requires = \
['netaddr>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['pktperf = pktperf.pktperf:main']}

setup_kwargs = {
    'name': 'pktperf',
    'version': '0.1.10',
    'description': 'pktgen scripts tool',
    'long_description': None,
    'author': 'junka',
    'author_email': 'wan.junjie@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/junka/pktperf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
