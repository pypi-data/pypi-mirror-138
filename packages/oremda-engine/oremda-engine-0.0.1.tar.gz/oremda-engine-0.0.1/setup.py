# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oremda',
 'oremda.engine',
 'oremda.engine.rpc',
 'oremda.engine.rpc.displays',
 'oremda.engine.rpc.messages',
 'oremda.engine.rpc.models',
 'oremda.engine.rpc.observer']

package_data = \
{'': ['*']}

install_requires = \
['fastapi-websocket-rpc>=0.1.21,<0.2.0',
 'msgpack>=1.0.3,<2.0.0',
 'oremda-cli>=0.0.1,<0.0.2',
 'oremda-core>=0.0.1,<0.0.2']

entry_points = \
{'oremda.cli.plugin': ['engine = oremda.engine.cli:main']}

setup_kwargs = {
    'name': 'oremda-engine',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Alessandro Genova',
    'author_email': 'alessandro.genova@kitware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
