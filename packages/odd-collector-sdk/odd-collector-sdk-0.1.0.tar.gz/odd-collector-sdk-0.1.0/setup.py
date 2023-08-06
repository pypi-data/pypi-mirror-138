# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_collector_sdk', 'odd_collector_sdk.api', 'odd_collector_sdk.domain']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler>=3.8.1,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'black>=21.12b0,<22.0',
 'odd-models>=1.0.14,<2.0.0',
 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'odd-collector-sdk',
    'version': '0.1.0',
    'description': 'ODD Collector',
    'long_description': "# ODD Collector SDK\n##### Root project for ODD collectors\n\n### Domain\n\n* CollectorConfig\n    Main model for collector\n\n* Plugin\n* AbstractAdapter\n\n\n### How to use\nThe main class for using is Collector.\n\n__Args__\nconfig_path: str - path to collector_config.yaml ('/collector_config.yaml')\nroot_package: str - root package for adapters which will be loaded ('aws_collector.adapters')\nplugins_union_type - needs to dynamicly create CollectorConfig model",
    'author': 'Open Data Discovery',
    'author_email': 'pypi@opendatadiscovery.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/opendatadiscovery/odd-collector-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.12',
}


setup(**setup_kwargs)
