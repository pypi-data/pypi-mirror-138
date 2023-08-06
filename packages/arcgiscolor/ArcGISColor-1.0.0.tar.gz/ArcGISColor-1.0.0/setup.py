# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcgiscolor']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.6.3,<3.0.0']

setup_kwargs = {
    'name': 'arcgiscolor',
    'version': '1.0.0',
    'description': 'Toolset to apply coloring to a layer in an ArcGIS Pro map, using the greedy color method',
    'long_description': None,
    'author': 'Cody Scott',
    'author_email': 'jcodyscott@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
