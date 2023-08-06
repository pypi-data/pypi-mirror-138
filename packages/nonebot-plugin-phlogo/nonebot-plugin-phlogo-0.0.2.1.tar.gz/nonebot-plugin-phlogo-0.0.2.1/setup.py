# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_phlogo']

package_data = \
{'': ['*'], 'nonebot_plugin_phlogo': ['resource/*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0',
 'nonebot-adapter-onebot==2.0.0-beta.1',
 'nonebot2==2.0.0-beta.1']

setup_kwargs = {
    'name': 'nonebot-plugin-phlogo',
    'version': '0.0.2.1',
    'description': '生成ph风格logo',
    'long_description': None,
    'author': 'kexue',
    'author_email': 'x@kexue.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3',
}


setup(**setup_kwargs)
