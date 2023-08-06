# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_termo']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['termo = my_termo.main:termo']}

setup_kwargs = {
    'name': 'my-termo',
    'version': '0.2.0',
    'description': 'A simple termo in command line style',
    'long_description': '# my-termo\n\n![termo](termo.gif)\n\nThis is a simple Termo application in command line style. This app run a Linux crontab task every day to get a new word. Type termo in your terminal to guess the daily word 😄😄😄 \n\n## Install ✨\nTo install termo command line type this\n```shell\npip install my-termo\n```\n\n## Development Instructions ⚒️\n\nFollow the below instructions to collaborate or run in development mode\n\n### Dependencies 🧒\n* `poetry` \n* `python`\n\n### Running 🏃\n\nTo install type this command\n```shell\npoetry install\n```\n\nRun termo\n```shell\ntermo\n```\n\n## Collaborate 💛💛💛\n\nSend issues or insights.',
    'author': 'Gustavo Soares',
    'author_email': 'gustavo.soares.cdc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GussSoares/my-termo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
