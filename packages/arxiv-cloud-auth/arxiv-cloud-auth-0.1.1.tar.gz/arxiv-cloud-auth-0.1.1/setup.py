# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arxiv', 'arxiv.cloud_auth', 'arxiv.cloud_auth.fastapi']

package_data = \
{'': ['*']}

install_requires = \
['CacheControl>=0.12.10,<0.13.0',
 'PyJWT>=2.3,<3.0',
 'SQLAlchemy>=1.4,<2.0',
 'google-auth>=2.6.0,<3.0.0']

setup_kwargs = {
    'name': 'arxiv-cloud-auth',
    'version': '0.1.1',
    'description': 'Minimal auth for arxiv',
    'long_description': None,
    'author': 'Brian D. Caruso',
    'author_email': 'bdc34@cornell.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
