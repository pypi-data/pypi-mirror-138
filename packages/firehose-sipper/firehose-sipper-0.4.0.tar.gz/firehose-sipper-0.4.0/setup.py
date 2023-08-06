# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['firehose_sipper']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.20.54,<2.0.0']

setup_kwargs = {
    'name': 'firehose-sipper',
    'version': '0.4.0',
    'description': 'Parses firehosed json from S3',
    'long_description': None,
    'author': 'Bob Gregory',
    'author_email': 'bob@codefiend.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
