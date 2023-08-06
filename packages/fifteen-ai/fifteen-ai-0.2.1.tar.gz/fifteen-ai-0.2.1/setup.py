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
    'version': '0.2.1',
    'description': 'TTS (text-to-speech) by 15.ai',
    'long_description': '# fifteen-ai\nTTS (text-to-speech) by 15.ai\n\n```shell\npip install fifteen_ai\n```\n\n```python\nimport fifteen_ai\n\nfifteen_ai.tts("I\'m sorry Dave. You can\'t do that.", "Twilight Sparkle")\n```\n\n```shell\npython -m fifteen_ai "I\'m sorry Dave. You can\'t do that."\n```\n',
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
