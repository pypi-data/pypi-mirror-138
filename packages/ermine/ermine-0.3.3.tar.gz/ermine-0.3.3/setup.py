# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ermine', 'ermine.plugs']

package_data = \
{'': ['*']}

install_requires = \
['multidict>=6.0.2,<7.0.0', 'pydantic>=1.9.0,<2.0.0', 'wire-rxtr>=0.2.2,<0.3.0']

setup_kwargs = {
    'name': 'ermine',
    'version': '0.3.3',
    'description': 'Nimble as an ermine',
    'long_description': '',
    'author': 'cheetahbyte',
    'author_email': 'bernerdoodle@outlook.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
