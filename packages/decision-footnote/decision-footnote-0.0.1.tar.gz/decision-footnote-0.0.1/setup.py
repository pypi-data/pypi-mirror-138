# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decision_footnote']

package_data = \
{'': ['*']}

install_requires = \
['lawsql-utils>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'decision-footnote',
    'version': '0.0.1',
    'description': 'Split html style sup-footnotes to validated list of dicts',
    'long_description': 'None',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
