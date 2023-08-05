# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['configator']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['configator = configator.main:app']}

setup_kwargs = {
    'name': 'pyconfigator',
    'version': '1.0.3',
    'description': 'A Configuration File Generator for GatorGradle',
    'long_description': "# ConfiGator\n\n![Mr.ConfiGator himself](img/icon.png)\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n[![Lint and Test](https://github.com/cmpsc-481-s22-m1/ConfiGator/actions/workflows/main.yml/badge.svg?branch=release%2F0.1.0)](https://github.com/cmpsc-481-s22-m1/ConfiGator/actions/workflows/main.yml)\n\nA configuration file generator meant to be used with [GatorGradle](https://github.com/GatorEducator/gatorgradle).\n\n## Overview\n\nConfiGator is a tool to be used in hand with GatorGradle to generate configuration\nfiles for assignments that require GatorGradle. ConfiGator uses\n[Poetry](https://python-poetry.org/) for package and dependency management.\n\n## Usage\n\n### Installing ConfiGator\n\nCommand to install ConfiGator\n\n```bash\npipx install pyconfigator\n```\n\n* *if* `pipx` *does not work, use* `pip` *instead.*\n\n### Running ConfiGator\n\nCommand to run ConfiGator (after installing using `pip` or `pipx`)\n\n```bash\nconfigator\n```\n\n### Command to Change Specific Configurations\n\nThe command below will show a list of every available command to change\nspecific configurations in `config/gatorgrader.yml` or `build.gradle`.\n\n```bash\nconfigator --help\n```\n\n### If you need Assistance\n\nCreate an issue or a discussion post for assistance if you encounter any issues\nwith ConfiGator.\n\n### Contributors\n\n* William Connelly, [@connellyw](https://github.com/connellyw)\n* Kyrie Doniz, [@donizk](https://github.com/donizk)\n* Kevin Lee, [@Kevin487](https://github.com/Kevin487)\n* Peter Snipes, [@Peter-Snipes](https://github.com/Peter-Snipes)\n* Kai'lani Woodard, [@kailaniwoodard](https://github.com/kailaniwoodard)\n* Adam Shinomiya, [@TheShiny1](https://github.com/TheShiny1)\n* Maria Kim Heinert, [@mariakimheinert](https://github.com/mariakimheinert)\n* Saejin Heinert, [@Michionlion](https://github.com/Michionlion)\n",
    'author': 'Kyrie Doniz',
    'author_email': None,
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
