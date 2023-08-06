# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['propan',
 'propan.annotations',
 'propan.config',
 'propan.db',
 'propan.db.workers',
 'propan.db.workers.implementation',
 'propan.db.workers.implementation.alchemy',
 'propan.db.workers.implementation.tortoise',
 'propan.db.workers.model',
 'propan.event_bus',
 'propan.event_bus.adapter',
 'propan.event_bus.model',
 'propan.fetch',
 'propan.fetch.fetcher',
 'propan.fetch.fetcher.adapter',
 'propan.fetch.fetcher.model',
 'propan.fetch.proxy',
 'propan.fetch.proxy.adapter',
 'propan.fetch.proxy.model',
 'propan.fetch.user_agent',
 'propan.logger',
 'propan.logger.adapter',
 'propan.logger.model',
 'propan.supervisors']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'aio-pika>=6.8.0,<7.0.0',
 'aiohttp>=3.7.4.post0,<4.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.8.2,<2.0.0',
 'uvloop>=0.16.0,<0.17.0',
 'watchgod>=0.6,<0.7']

entry_points = \
{'console_scripts': ['propan = propan:run']}

setup_kwargs = {
    'name': 'propan',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'PasNA6713',
    'author_email': 'diementros@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
