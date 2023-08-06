# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oremda', 'oremda.api']

package_data = \
{'': ['*']}

install_requires = \
['oremda-core>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'oremda-api',
    'version': '0.0.2',
    'description': '',
    'long_description': '',
    'author': 'Alessandro Genova',
    'author_email': 'alessandro.genova@kitware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
