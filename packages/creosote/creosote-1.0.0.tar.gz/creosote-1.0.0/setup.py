# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['creosote']

package_data = \
{'': ['*']}

install_requires = \
['distlib>=0.3.4,<0.4.0', 'loguru>=0.6.0,<0.7.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['creosote = creosote.cli:main']}

setup_kwargs = {
    'name': 'creosote',
    'version': '1.0.0',
    'description': 'Identify unused dependencies and avoid a bloated virtual environment.',
    'long_description': None,
    'author': 'Fredrik Averpil',
    'author_email': 'fredrik.averpil@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
