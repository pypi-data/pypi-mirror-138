# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kapow', 'kapow.cli', 'kapow.cli.resources', 'kapow.resources']

package_data = \
{'': ['*']}

install_requires = \
['docopt-ng>=0.7.2,<0.8.0', 'rich>=11.2.0,<12.0.0', 'tomlkit>=0.9.2,<0.10.0']

entry_points = \
{'console_scripts': ['kapow = kapow.cli:main']}

setup_kwargs = {
    'name': 'kapow',
    'version': '0.1.1',
    'description': '',
    'long_description': '### kapow\n\n\nA python application launch framework with a punch! Kapow!\n\n**This alpha software currently under active development**\n',
    'author': 'Mark Gemmill',
    'author_email': 'mark@markgemmill.com',
    'maintainer': 'Mark Gemmill',
    'maintainer_email': 'dev@markgemmill.com',
    'url': 'https://github.com/markgemmill/kapow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
