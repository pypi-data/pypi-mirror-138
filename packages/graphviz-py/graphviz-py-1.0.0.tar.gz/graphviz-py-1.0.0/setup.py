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
    'version': '1.0.0',
    'description': 'Allows Python code execution inside of graphviz diagrams.',
    'long_description': '# graphviz-py\n[![package version](https://img.shields.io/pypi/v/graphviz-py?style=flat-square)](https://pypi.org/project/graphviz-py/)\n[![py versions](https://img.shields.io/pypi/pyversions/graphviz-py?style=flat-square)](https://pypi.org/project/graphviz-py/)\n[![license](https://img.shields.io/github/license/Alwinator/graphviz-py?style=flat-square)](LICENSE)\n\nAllows Python code execution inside of [graphviz](https://graphviz.org/) diagrams\n\n## Example\n```dot\ngraph python_graph {\n{{\nimport math\n\nvalue = 0.5\nsin = math.sin(value)\ncos = math.cos(value)\n}}\n\n    A [label="{{= value }}"];\n    B [label="{{= sin }}"];\n    C [label="{{= cos }}"];\n\n    A -- B;\n    A -- C;\n}\n```\n\n### Output\n![output](assets/output.svg)\n\n## Install\n```bash\npip install graphviz-py\n```\n\n**Important: Make sure graphviz is installed!** See [graphviz installation instructions](https://graphviz.org/download/).\n\n\n## Usage\n### Using files\n```bash\ngraphviz-py -Tsvg example/example.py.dot -o output.svg\ngraphviz-py -Tpng example/example.py.dot -o output.png\n```\n\n### Using stdin / pipes\n```bash\necho \'digraph { A -> B [label="{{= 38 * 73 }}"] }\' | graphviz-py -Tsvg > output.svg\n```\n\ngraphviz-py passes all unknown arguments to graphviz. So you can use all [graphviz arguments](https://graphviz.org/doc/info/command.html).\n\n## Coming soon\n- Compartibility with asciidoctor-diagram\n',
    'author': 'Alwin Schuster',
    'author_email': 'contact@alwinschuster.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Alwinator/graphviz-py',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0',
}


setup(**setup_kwargs)
