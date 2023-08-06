# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typing_environs']

package_data = \
{'': ['*']}

install_requires = \
['easydict>=1.9,<2.0', 'environs>=9.5.0,<10.0.0', 'pydantic>=0.0.0,<0.0.1']

setup_kwargs = {
    'name': 'typing-environs',
    'version': '0.1.0',
    'description': '### typing_environs add type hints support  for environs',
    'long_description': '### FastTask framework\nFastTask is simple to fast run task\n\n#### install\n`pip install fasttask`\n',
    'author': 'Euraxluo',
    'author_email': 'euraxluo@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Euraxluo/typing_environs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
