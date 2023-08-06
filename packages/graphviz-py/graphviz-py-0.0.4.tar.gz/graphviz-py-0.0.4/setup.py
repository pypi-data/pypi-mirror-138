# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphviz_py']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['graphviz-py = graphviz_py.cli:main']}

setup_kwargs = {
    'name': 'graphviz-py',
    'version': '0.0.4',
    'description': 'Allows Python code execution inside of graphviz diagrams.',
    'long_description': None,
    'author': 'Alwin Schuster',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Alwinator/graphviz-py',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0',
}


setup(**setup_kwargs)
