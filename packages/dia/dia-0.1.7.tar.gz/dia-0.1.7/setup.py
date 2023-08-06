# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dia']

package_data = \
{'': ['*']}

install_requires = \
['click-config-file>=0.6.0,<0.7.0', 'click>=8,<9']

entry_points = \
{'console_scripts': ['dia = dia.cli:cli']}

setup_kwargs = {
    'name': 'dia',
    'version': '0.1.7',
    'description': 'Dia is a work log, letting you easily keep a history of what you worked on.',
    'long_description': 'Dia\n===\n\nHave you ever spent a long day at work, only to wonder at the end of it what you\nactually got done? Do you wish you remembered why you made a decision way back when?\nDo you want to find the day you worked on a specific thing, but haven\'t left any trace?\n\nDia solves all those problems by helping you keep a work diary.\n\n\nInstallation\n------------\n\nInstalling Dia is simple. You can use `pipx` (recommended):\n\n```bash\n$ pipx install dia\n```\n\nOr `pip` (less recommended):\n\n```bash\n$ pip install dia\n```\n\n\nUsage\n-----\n\nTo log a task you\'ve completed, you can use `dia log`:\n\n```bash\n$ dia log "Completed the diary feature."\n```\n\nThis will generate the following `diary.txt` in the current directory (or append to it\nif it already exists):\n\n```md\nWork diary\n==========\n\n\n2022-02-09\n----------\n\n* Completed the diary feature.\n```\n\nIf you want to specify a fixed file to always work on, you can do that by setting the\n`diary` option in `~/.config/dia/config`:\n\n```ini\ndiary="/home/stavros/diary.txt"\n```\n\nYou can similarly override any other options.\n\n\nSemantic tags\n-------------\n\nDia supports (though currently very tenuously) semantic tags. This means it can\nunderstand people, projects, and tags. For example, you can say:\n\n```bash\n$ dia log "Worked on the %Dia #data-model with @JohnK."\n```\n\nYou can show all items with:\n\n```bash\n$ dia show projects\n\nProjects\n========\n* Dia\n* Foo\n* Bar\n* Baz\n```\n\nSame with `tags` and `people`.\n\n# Changelog\n\n\n## v0.1.7 (2022-02-16)\n\n### Features\n\n* Add the "standup" command. [Stavros Korokithakis]\n\n* Add the "show people|tags|projects" commands. [Stavros Korokithakis]\n\n* Allow passing a regex to the "search" command. [Stavros Korokithakis]\n\n* Add the "edit" command. [Stavros Korokithakis]\n\n### Fixes\n\n* Reduce whitespace between elements. [Stavros Korokithakis]\n\n\n## v0.1.6 (2022-02-11)\n\n### Features\n\n* Refactor "show" and add "show previous" command. [Stavros Korokithakis]\n\n### Fixes\n\n* Don\'t use pager on search. [Stavros Korokithakis]\n\n* Don\'t show empty days in the "search" command. [Stavros Korokithakis]\n\n\n## v0.1.5 (2022-02-11)\n\n### Features\n\n* Wrap long task text. [Stavros Korokithakis]\n\n* Add "search" command. [Stavros Korokithakis]\n\n### Fixes\n\n* Fix diary config name. [Stavros Korokithakis]\n\n* Don\'t crash if there are no tasks. [Stavros Korokithakis]\n\n\n## v0.1.4 (2022-02-10)\n\n### Features\n\n* Add "show" command. [Stavros Korokithakis]\n\n\n',
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
