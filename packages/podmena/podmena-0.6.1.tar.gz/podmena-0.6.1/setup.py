# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['podmena']

package_data = \
{'': ['*'], 'podmena': ['resources/*']}

install_requires = \
['click>=8.0,<9.0']

entry_points = \
{'console_scripts': ['podmena = podmena.cli:cli']}

setup_kwargs = {
    'name': 'podmena',
    'version': '0.6.1',
    'description': 'Enhance your commit messages with emoji',
    'long_description': '<h2 align="center">podmena</h2>\n\n<p align="center">\n  <a href="https://github.com/bmwant/podmena/actions">\n    <img alt="Checks" src="https://github.com/bmwant/podmena/actions/workflows/tests.yml/badge.svg">\n  </a>\n\n  <a href="https://pypi.org/project/podmena/">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/podmena">\n  </a>\n\n  <a href="https://github.com/psf/black">\n    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n  </a>\n</p>\n<p align="center">\nEnhance your commit messages with emoji 🍒\n</p>\n\npodmena will automatically add random emoji to every commit message for any\ngit repository installed for.\n\n![emoji](https://github.com/bmwant/podmena/blob/main/podmena.png)\n\n**868** items in database so far!\n\nCredits go to [WebFX](https://www.webfx.com/tools/emoji-cheat-sheet/) for list of emoji!\n\n### Installation\n\n```bash\n$ pip install podmena\n```\n\n* Activate for current git repository\n\n```bash\n$ podmena add local\n```\n\nYou can also replace `add` with a different alias\n\n`activate` / `enable` / `install` / `on`\n\ne.g. `podmena enable local`\n\n* Activate globally for all repositories (works with git `2.9.1` and above)\n\n```bash\n$ git --version\n$ podmena add global  # Aliases work here as well\n```\n\n* Deactivate it\n```bash\n$ podmena rm local\n$ podmena rm global\n```\n\nYou can replace `rm` with any of these available aliases\n\n`remove` / `delete` / `deactivate` / `disable` / `off` / `uninstall`\n\ne.g. `podmena deactivate local`\n\n* Check current status if you not sure\n\n```bash\n$ podmena status\n```\n\n* And finally `podmena --version` and `podmena --help` in case you need more\ndetails.\n\n> **NOTE:** uninstalling globally will not remove hooks from repositories where\nit was installed locally. You need to switch to that directory manually and uninstall it locally as well.\n\n### Preview\n\nSee [PREVIEW.md](https://github.com/bmwant/podmena/blob/main/PREVIEW.md) for the full list of icons in the database and to check how GitHub renders them.\n### Contribute\n\nSee [DEVELOP.md](https://github.com/bmwant/podmena/blob/main/DEVELOP.md) to setup your local development environment and feel free to create a pull request with a new feature.\n\n### Releases\n\nSee [CHANGELOG.md](https://github.com/bmwant/podmena/blob/main/CHANGELOG.md) for the new features included within each release.\n\n### See also\n\n* [GitHooks](https://githooks.com/)\n* [Atlassian tutorial for git hooks](https://www.atlassian.com/git/tutorials/git-hooks)\nThanks [@kakovskyi](https://github.com/kakovskyi) working for Atlassian!\n* It\'s a wrong place to search if you are looking for 🍋 lemonparty.fun 🍋 club\n\n### Say thanks!\n\n🐶 `D7DA74qzZUyh9cctCxWovPTEovUSjGzL2S` this is [Dogecoin](https://dogecoin.com/) wallet to support the project.\n',
    'author': 'Misha Behersky',
    'author_email': 'bmwant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bmwant/podmena',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
