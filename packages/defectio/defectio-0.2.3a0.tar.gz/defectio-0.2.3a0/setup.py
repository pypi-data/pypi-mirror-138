# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['defectio',
 'defectio.ext.commands',
 'defectio.ext.tasks',
 'defectio.models',
 'defectio.types']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7,<0.9',
 'aiohttp>=3.7.4,<4.0.0',
 'msgpack>=1.0.2,<2.0.0',
 'orjson>=3.6.3,<4.0.0',
 'ulid-py>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'defectio',
    'version': '0.2.3a0',
    'description': 'Wrapper for Revolt API',
    'long_description': '# Defectio\n\n![revolt-api](https://img.shields.io/npm/v/revolt-api?label=Revolt%20API) [![Documentation Status](https://readthedocs.org/projects/defectio/badge/?version=latest)](https://defectio.readthedocs.io/en/latest/?badge=latest) [![All Contributors](https://img.shields.io/badge/all_contributors-7-orange.svg)](#contributors-)\n\n\n**defectio** is a direct implementation of the entire Revolt API and provides a way to authenticate and start communicating with Revolt servers. Similar interface to discord.py\n\n## Example Usage\n\n```python3\nimport defectio\n\nclient = defectio.Client()\n\n\n@client.event\nasync def on_ready():\n    print("We have logged in.")\n\n\n@client.event\nasync def on_message(message: defectio.Message):\n    if message.author == client.user:\n        return\n    if message.content.startswith("$hello"):\n        await message.channel.send("Hello!")\n\n\nclient.run("your token here")\n```\n\n## Contribute\n\nJoin our server [here](https://app.revolt.chat/invite/FfbwgFDk)\n\n## License\n\nLicensed under an MIT license\n\nBased on discord.py by Rapptz [here](https://github.com/Rapptz/discord.py)\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://github.com/nixonjoshua98"><img src="https://avatars.githubusercontent.com/u/22799825?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Joshua Nixon</b></sub></a><br /><a href="https://github.com/Darkflame72/defectio/commits?author=nixonjoshua98" title="Code">💻</a></td>\n    <td align="center"><a href="https://github.com/LimeProgramming"><img src="https://avatars.githubusercontent.com/u/29736217?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Adam</b></sub></a><br /><a href="https://github.com/Darkflame72/defectio/commits?author=LimeProgramming" title="Code">💻</a></td>\n    <td align="center"><a href="https://github.com/jottew"><img src="https://avatars.githubusercontent.com/u/71946106?v=4?s=100" width="100px;" alt=""/><br /><sub><b>jotte</b></sub></a><br /><a href="https://github.com/Darkflame72/defectio/commits?author=jottew" title="Code">💻</a></td>\n    <td align="center"><a href="https://insrt.uk"><img src="https://avatars.githubusercontent.com/u/38285861?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Paul Makles</b></sub></a><br /><a href="https://github.com/Darkflame72/defectio/issues?q=author%3Ainsertish" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="https://github.com/Cearaj"><img src="https://avatars.githubusercontent.com/u/75398448?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Cearaj</b></sub></a><br /><a href="https://github.com/Darkflame72/defectio/commits?author=Cearaj" title="Code">💻</a></td>\n    <td align="center"><a href="https://github.com/jafreli"><img src="https://avatars.githubusercontent.com/u/31709372?v=4?s=100" width="100px;" alt=""/><br /><sub><b>jafreli</b></sub></a><br /><a href="https://github.com/Darkflame72/defectio/commits?author=jafreli" title="Code">💻</a></td>\n    <td align="center"><a href="https://dark42ed.cf/"><img src="https://avatars.githubusercontent.com/u/74568473?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Dark42ed</b></sub></a><br /><a href="https://github.com/Darkflame72/defectio/commits?author=Dark42ed" title="Documentation">📖</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n',
    'author': 'Leon Bowie',
    'author_email': 'leon@bowie-co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Darkflame72/defectio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
