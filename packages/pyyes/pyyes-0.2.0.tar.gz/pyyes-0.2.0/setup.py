# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yes']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.2.0,<3.0.0',
 'cryptography>=35.0.0,<36.0.0',
 'furl>=2.1.3,<3.0.0',
 'pyHanko[pkcs11]==0.8.0']

setup_kwargs = {
    'name': 'pyyes',
    'version': '0.2.0',
    'description': 'yes® Relying Party/Client Implementation in Python 3',
    'long_description': None,
    'author': 'Daniel Fett',
    'author_email': 'danielf@yes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
