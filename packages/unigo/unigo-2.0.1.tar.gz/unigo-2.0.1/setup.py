# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unigo',
 'unigo.api',
 'unigo.api.store',
 'unigo.api.store.cache',
 'unigo.repl',
 'unigo.repl.commands',
 'unigo.tree']

package_data = \
{'': ['*'], 'unigo': ['data/*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'Owlready2>=0.36,<0.37',
 'docopt>=0.6.2,<0.7.0',
 'marshmallow>=3.14.1,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'requires>=0.10.2,<0.11.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'unigo',
    'version': '2.0.1',
    'description': '',
    'long_description': None,
    'author': 'glaunay',
    'author_email': 'pitooon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
