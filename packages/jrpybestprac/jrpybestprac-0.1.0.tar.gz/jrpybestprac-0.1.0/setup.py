# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpybestprac', 'jrpybestprac.examples']

package_data = \
{'': ['*'], 'jrpybestprac': ['data/*']}

install_requires = \
['black>=22.1',
 'matplotlib>=3.0',
 'pandas>=1',
 'pep8-naming>=0.12',
 'pyjanitor>=0.22',
 'reprexpy<=1',
 'seaborn>=0.11']

setup_kwargs = {
    'name': 'jrpybestprac',
    'version': '0.1.0',
    'description': 'Jumping Rivers: Python Best Practices',
    'long_description': None,
    'author': 'Jack Walton',
    'author_email': 'jack@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
