# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pythonanywhere_core']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cov>=3.0.0,<4.0.0', 'pytest>=7.0.0,<8.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pythonanywhere-core',
    'version': '0.1.0',
    'description': 'API wrapper for programmatic management of PythonAnywhere services.',
    'long_description': 'API wrapper for programmatic management of PythonAnywhere services.',
    'author': 'PythonAnywhere',
    'author_email': 'developers@pythonanywhere.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
