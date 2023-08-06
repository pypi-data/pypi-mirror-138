# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boto3_oversize', 'boto3_oversize.tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3-stubs[sqs,sns,s3]>=1.20.30', 'boto3>=1.20.30']

setup_kwargs = {
    'name': 'boto3-oversize',
    'version': '0.1.1',
    'description': 'Transparently stores oversize SNS messages in S3 and retrieves them when receiving messages using SQS.',
    'long_description': None,
    'author': 'roberthl',
    'author_email': 'roberthl@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
