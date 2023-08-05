# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dia']

package_data = \
{'': ['*']}

install_requires = \
['click>=8,<9']

entry_points = \
{'console_scripts': ['dia = dia.cli:cli']}

setup_kwargs = {
    'name': 'dia',
    'version': '0.1.0',
    'description': 'Dia is a work log, letting you easily keep a history of what you worked on.',
    'long_description': 'Dia\n===\n\nDia lets you keep a work log.\n\n\nInstallation\n------------\n\nInstalling Dia is simple. You can use `pipx` (recommended):\n\n```\n$ pipx install dia\n```\n\nOr `pip` (less recommended):\n\n```\n$ pip install dia\n```\n',
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/stavros/dia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
