# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fifteen_ai']

package_data = \
{'': ['*']}

install_requires = \
['playsound>=1.3.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'fifteen-ai',
    'version': '0.1.0',
    'description': 'TTS by 15.ai',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
