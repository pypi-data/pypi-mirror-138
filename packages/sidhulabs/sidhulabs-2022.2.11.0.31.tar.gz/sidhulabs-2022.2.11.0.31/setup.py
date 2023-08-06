# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sidhulabs', 'sidhulabs.elastic']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=8,<9']

setup_kwargs = {
    'name': 'sidhulabs',
    'version': '2022.2.11.0.31',
    'description': 'Common Python utility functions',
    'long_description': None,
    'author': 'Ashton Sidhu',
    'author_email': 'ashton.sidhu1994@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
