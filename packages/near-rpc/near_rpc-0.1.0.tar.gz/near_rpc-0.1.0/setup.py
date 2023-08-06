# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['near_rpc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'near-rpc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Marcelo Fornet',
    'author_email': 'mfornet94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
