# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oremda', 'oremda.cli']

package_data = \
{'': ['*']}

install_requires = \
['click-plugins>=1.1.1,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'docker>=5.0.3,<6.0.0',
 'oremda-core>=0.0.1,<0.0.2',
 'requests>=2.27.1,<3.0.0',
 'spython>=0.1.17,<0.2.0']

entry_points = \
{'console_scripts': ['oremda = oremda.cli:main'],
 'oremda.cli.plugin': ['pull = oremda.cli.pull:main',
                       'run = oremda.cli.run:main']}

setup_kwargs = {
    'name': 'oremda-cli',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Alessandro Genova',
    'author_email': 'alessandro.genova@kitware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
