# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acquisition_case_transform']

package_data = \
{'': ['*']}

install_requires = \
['citation-date>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'acquisition-case-transform',
    'version': '0.1.1',
    'description': 'Fix typograpic errors / non-standard Supreme Court citations',
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
