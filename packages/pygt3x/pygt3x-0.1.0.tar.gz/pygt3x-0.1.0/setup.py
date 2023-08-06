# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygt3x']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.2,<2.0.0', 'pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'pygt3x',
    'version': '0.1.0',
    'description': 'Python module for reading GT3X/AGDC file format data',
    'long_description': None,
    'author': 'Mark Fogle',
    'author_email': 'mark.fogle@theactigraph.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
