# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocstr', 'mkdocstr.langs', 'mkdocstr.output_styles']

package_data = \
{'': ['*']}

install_requires = \
['Mako>=1.1.6,<2.0.0', 'attrs>=21.4.0,<22.0.0', 'tree-sitter>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['mkdocstr = mkdocstr.cli:main']}

setup_kwargs = {
    'name': 'mkdocstr',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jethro Kuan',
    'author_email': 'jethrokuan95@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
