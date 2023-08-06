# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bgenv']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.8.0,<2.0.0',
 'folium>=0.12.1,<0.13.0',
 'geopandas>=0.10.2,<0.11.0',
 'igraph>=0.9.9,<0.10.0',
 'networkx==2.6.2',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'bgenv',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
