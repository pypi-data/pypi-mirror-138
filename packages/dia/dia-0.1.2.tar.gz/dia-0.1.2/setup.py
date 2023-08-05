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
    'version': '0.1.2',
    'description': 'Dia is a work log, letting you easily keep a history of what you worked on.',
    'long_description': 'Dia\n===\n\nHave you ever spent a long day at work, only to wonder at the end of it what you\nactually got done? Do you wish you remembered why you made a decision way back when?\nDo you want to find the day you worked on a specific thing, but haven\'t left any trace?\n\nDia solves all those problems by helping you keep a work diary.\n\n\nInstallation\n------------\n\nInstalling Dia is simple. You can use `pipx` (recommended):\n\n```bash\n$ pipx install dia\n```\n\nOr `pip` (less recommended):\n\n```bash\n$ pip install dia\n```\n\n\nUsage\n-----\n\nTo log a task you\'ve completed, you can use `dia log`:\n\n```bash\n$ dia log "Completed the diary feature."\n```\n\nThis will generate the following `log.txt` in the current directory (or append to it if\nit already exists):\n\n```md\nWork diary\n==========\n\n\n2022-02-09\n----------\n\n* Completed the diary feature.\n```\n\n# Changelog\n\n\n## v0.1.2 (2022-02-09)\n\n### Fixes\n\n* Fix the help text for the "log" command. [Stavros Korokithakis]\n\n\n## v0.1.1 (2022-02-09)\n\n### Fixes\n\n* Don\'t die if the diary file doesn\'t exist. [Stavros Korokithakis]\n\n\n## v0.1.0 (2022-02-09)\n\n### Fixes\n\n* Fix program symlink. [Stavros Korokithakis]\n\n* Fix program symlink. [Stavros Korokithakis]\n\n\n',
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
