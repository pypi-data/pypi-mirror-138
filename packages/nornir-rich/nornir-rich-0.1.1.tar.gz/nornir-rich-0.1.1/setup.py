# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_rich']

package_data = \
{'': ['*']}

install_requires = \
['nornir>=3,<4', 'rich>=11.2.0,<12.0.0']

setup_kwargs = {
    'name': 'nornir-rich',
    'version': '0.1.1',
    'description': "Collection of 'nice looking' functions with rich for nornir",
    'long_description': None,
    'author': 'ubaumann',
    'author_email': 'github@m.ubaumann.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
