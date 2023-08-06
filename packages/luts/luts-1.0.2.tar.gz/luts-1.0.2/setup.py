# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['luts']

package_data = \
{'': ['*']}

install_requires = \
['netcdf4>=1.5.4', 'numpy>=1.19.2', 'scipy>=1.5.2', 'xarray>=0.16.1']

setup_kwargs = {
    'name': 'luts',
    'version': '1.0.2',
    'description': 'Multidimensional labeled arrays and datasets in Python, similar to xarray.',
    'long_description': None,
    'author': 'François Steinmetz',
    'author_email': 'fs@hygeos.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
