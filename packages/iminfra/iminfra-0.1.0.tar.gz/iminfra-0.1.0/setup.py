# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['iminfra', 'iminfra.cli']

package_data = \
{'': ['*']}

install_requires = \
['pulumi>=3.24.1,<4.0.0']

entry_points = \
{'console_scripts': ['iminfra = iminfra.cli.main:main']}

setup_kwargs = {
    'name': 'iminfra',
    'version': '0.1.0',
    'description': 'Intermine infrastructure as code.',
    'long_description': None,
    'author': 'Ankur Kumar',
    'author_email': 'ank@leoank.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
