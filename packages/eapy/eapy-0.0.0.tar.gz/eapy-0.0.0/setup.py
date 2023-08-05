# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eapy']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib', 'numpy>=1.22,<1.23', 'ray>=1.10,<1.11']

setup_kwargs = {
    'name': 'eapy',
    'version': '0.0.0',
    'description': 'Evolutionary Algorithm for Python',
    'long_description': None,
    'author': 'Dennis Otter',
    'author_email': 'dennis.john.otter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
