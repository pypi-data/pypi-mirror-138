# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyproteins',
 'pyproteins.alignment',
 'pyproteins.container',
 'pyproteins.sequence',
 'pyproteins.utils']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79,<2.0',
 'bs4>=0.0.1,<0.0.2',
 'lxml>=4.7.1,<5.0.0',
 'numpy>=1.22.2,<2.0.0']

setup_kwargs = {
    'name': 'pyproteins',
    'version': '2.0.0',
    'description': 'General purpose bionformatics library',
    'long_description': None,
    'author': 'glaunay',
    'author_email': 'pitooon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
