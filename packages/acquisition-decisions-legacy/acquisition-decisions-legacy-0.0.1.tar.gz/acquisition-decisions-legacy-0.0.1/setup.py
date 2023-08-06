# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acquisition_decisions_legacy']

package_data = \
{'': ['*']}

install_requires = \
['acquisition-case-transform>=0.1.1,<0.2.0',
 'acquisition-ruling-phrase>=0.3.1,<0.4.0',
 'acquisition-sanitizer>=0.4.1,<0.5.0',
 'httpx>=0.21,<0.22']

setup_kwargs = {
    'name': 'acquisition-decisions-legacy',
    'version': '0.0.1',
    'description': "Processes decisions before 1996. The Philippine Supreme Court's digital library starts in 1996.",
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
