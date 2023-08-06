# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['github_webhooks', 'github_webhooks.handlers', 'github_webhooks.schemas']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.73.0,<0.74.0', 'pydantic[dotenv]>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'github-webhooks-framework',
    'version': '0.1.1',
    'description': 'GitHub Webhooks Framework',
    'long_description': None,
    'author': 'karech',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/karech/github-webhooks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
