# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['security_poc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'security-poc',
    'version': '0.2.0',
    'description': 'Just to test some security things',
    'long_description': None,
    'author': 'Marco Dennstädt',
    'author_email': 'Marco.Dennstaedt@zuehlke.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
