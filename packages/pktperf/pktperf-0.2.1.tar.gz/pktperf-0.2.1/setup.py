# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pktperf']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pktperf = pktperf.pktperf:main']}

setup_kwargs = {
    'name': 'pktperf',
    'version': '0.2.1',
    'description': 'pktgen scripts tool',
    'long_description': None,
    'author': 'junka',
    'author_email': 'wan.junjie@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/junka/pktperf',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
