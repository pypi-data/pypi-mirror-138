# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xblobs']

package_data = \
{'': ['*']}

install_requires = \
['dask-image>=0.2.0', 'numpy>=1.22.2', 'scipy>=1.2.0', 'xarray>=0.11.2']

setup_kwargs = {
    'name': 'xblobs',
    'version': '1.0.1',
    'description': 'Python tool to detect and analyse coherent structures in turbulence, powered by xarray.',
    'long_description': None,
    'author': 'gregordecristoforo',
    'author_email': 'gregor.decristoforo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uit-cosmo/xblobs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
