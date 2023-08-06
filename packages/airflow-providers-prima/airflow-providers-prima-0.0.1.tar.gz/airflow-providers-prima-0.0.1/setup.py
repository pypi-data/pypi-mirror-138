# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airflow_providers_prima']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'airflow-providers-prima',
    'version': '0.0.1',
    'description': 'python repository for commmons operators,hooks and utils for Apache Airflow',
    'long_description': None,
    'author': 'sceriol',
    'author_email': 'simone.cerioli@prima.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
