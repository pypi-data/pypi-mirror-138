# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['security_poc2']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'security-poc2',
    'version': '500.0.0',
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
