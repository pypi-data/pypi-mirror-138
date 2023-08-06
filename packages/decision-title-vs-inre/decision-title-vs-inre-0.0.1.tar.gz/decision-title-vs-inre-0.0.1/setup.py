# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decision_title_vs_inre',
 'decision_title_vs_inre.extras',
 'decision_title_vs_inre.indicators']

package_data = \
{'': ['*']}

install_requires = \
['lawsql-utils>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'decision-title-vs-inre',
    'version': '0.0.1',
    'description': 'Decision Title Parts and Lines via Regexes',
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
