# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spellsync', 'spellsync.dictionary']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['spellsync = spellsync.main:main']}

setup_kwargs = {
    'name': 'spellsync',
    'version': '0.1.0',
    'description': 'Synchronise personal spelling dictionaries across applications',
    'long_description': None,
    'author': 'Patrice Neff',
    'author_email': 'mail@patrice.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
