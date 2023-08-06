# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['SEAL']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.2,<2.0.0']

setup_kwargs = {
    'name': 'spline-algorithm-library',
    'version': '1.0.0',
    'description': 'A spline library written in Python',
    'long_description': None,
    'author': 'Ivar Stangeby',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
