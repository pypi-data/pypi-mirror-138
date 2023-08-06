# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_tea']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.12.0,<9.0.0',
 'prompt-toolkit>=3.0.24,<4.0.0',
 'returns>=0.18.0,<0.19.0',
 'rich>=11.0.0,<12.0.0']

setup_kwargs = {
    'name': 'rich-tea',
    'version': '0.3.0',
    'description': 'Tools for approximating The Elm Architecture, powered by Rich',
    'long_description': '# Tools for approximating The Elm Architecture, powered by Rich\n![Fzf demo](./fzf-demo.gif)\n',
    'author': 'Aatif Syed',
    'author_email': 'aatifsyedyp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aatifsyed/rich-tea',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
