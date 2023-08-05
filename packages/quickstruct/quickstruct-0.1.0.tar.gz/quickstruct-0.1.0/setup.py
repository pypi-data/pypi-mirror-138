# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickstruct']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'quickstruct',
    'version': '0.1.0',
    'description': 'A small library to ease the creation, usage, serialization and deserialization of C structs.',
    'long_description': None,
    'author': 'Binyamin Y Cohen',
    'author_email': 'binyamincohen555@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
