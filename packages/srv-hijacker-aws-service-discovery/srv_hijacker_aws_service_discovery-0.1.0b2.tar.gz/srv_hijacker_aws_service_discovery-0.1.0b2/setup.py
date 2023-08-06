# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['srv_hijacker']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.25.0,<0.26.0', 'dnspython>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'srv-hijacker-aws-service-discovery',
    'version': '0.1.0b2',
    'description': '',
    'long_description': None,
    'author': 'Andrei Shabanski',
    'author_email': 'shabanski.andrei@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
