# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leap_model_rebuilder']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'leap-model-rebuilder',
    'version': '0.1.2',
    'description': '',
    'long_description': '# leap-model-rebuilder\nKeras model rebuilder tool for model rebuilding with alterations\n',
    'author': 'dorhar',
    'author_email': 'doron.harnoy@tensorleap.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tensorleap/leap-model-rebuilder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
