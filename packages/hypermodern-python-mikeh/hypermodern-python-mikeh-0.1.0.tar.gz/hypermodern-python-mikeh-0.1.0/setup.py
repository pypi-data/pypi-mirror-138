# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.14.1,<4.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-python = hypermodern_python.console:main']}

setup_kwargs = {
    'name': 'hypermodern-python-mikeh',
    'version': '0.1.0',
    'description': 'Hypermodern Python Project',
    'long_description': '[![Tests](https://github.com/MichaelHarrison87/hypermodern-mikeh/workflows/Tests/badge.svg)](https://github.com/MichaelHarrison87/hypermodern-mikeh/actions?workflow=Tests)\n# hypermodern-mikeh\n',
    'author': 'MichaelHarrison87',
    'author_email': 'harrisoneighty7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MichaelHarrison87/hypermodern-mikeh',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
