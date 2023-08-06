# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fxh_my_app']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0', 'pymongo[srv]>=4.0.1,<5.0.0', 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'fxh-my-app',
    'version': '2.4.0',
    'description': '',
    'long_description': None,
    'author': 'juntao',
    'author_email': '61410813@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
