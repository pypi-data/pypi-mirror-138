# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfrost', 'dfrost.lib']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.20.51,<2.0.0',
 'cryptography>=36.0.1,<37.0.0',
 'pathspec>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['dfrost = frost.cli:run']}

setup_kwargs = {
    'name': 'dfrost',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'tlonny',
    'author_email': 't@lonny.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
