# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reqmap']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.26,<4.0.0',
 'click>=8.0.3,<9.0.0',
 'networkx>=2.6.3,<3.0.0',
 'pydot>=1.4.2,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'toolz>=0.11.2,<0.12.0']

entry_points = \
{'console_scripts': ['reqmap = reqmap.cli:cli']}

setup_kwargs = {
    'name': 'reqmap',
    'version': '0.2.0',
    'description': 'A package / CLI for mapping the dependencies of python projects',
    'long_description': '\n# Reqmap\n\nA package / CLI for mapping Python project dependencies, specifically by making\nit easier to convert them to Networkx / dot format for visualization.\n\n```\npip install\nreqmap graph my_project out.dot\n```\n',
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/peder2911/reqmap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
