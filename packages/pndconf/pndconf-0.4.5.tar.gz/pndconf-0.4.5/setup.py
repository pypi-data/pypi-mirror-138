# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pndconf']

package_data = \
{'': ['*']}

install_requires = \
['bibtexparser>=1.2.0,<2.0.0',
 'chardet>=4.0.0,<5.0.0',
 'common-pyutil>=0.8.0,<0.9.0',
 'pandoc-eqnos>=2.5.0,<3.0.0',
 'pandocfilters>=1.5.0,<2.0.0',
 'pyyaml>=5.4.0,<6.0.0',
 'watchdog>=2.1.5,<3.0.0']

entry_points = \
{'console_scripts': ['pndconf = pndconf.__main__:main']}

setup_kwargs = {
    'name': 'pndconf',
    'version': '0.4.5',
    'description': '',
    'long_description': None,
    'author': 'Akshay',
    'author_email': 'akshay.badola.cs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
