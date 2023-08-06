# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zetamarkets']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zetamarkets',
    'version': '0.0.1a0',
    'description': 'Coming on Saturday',
    'long_description': None,
    'author': 'Joel Lee',
    'author_email': 'joel@joellee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
