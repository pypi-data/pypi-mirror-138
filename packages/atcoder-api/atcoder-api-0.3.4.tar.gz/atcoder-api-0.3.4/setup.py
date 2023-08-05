# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['atcoder']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'aiodns',
 'aiohttp',
 'beautifulsoup4',
 'boto3',
 'cchardet',
 'lxml',
 'pandas',
 'requests',
 'selenium',
 'tqdm']

setup_kwargs = {
    'name': 'atcoder-api',
    'version': '0.3.4',
    'description': 'AtCoder API.',
    'long_description': '# AtCoder API for Python.\n\n\n\n## Documentation\nsee https://atcoder-api-python.readthedocs.io',
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://atcoder-api-python.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
