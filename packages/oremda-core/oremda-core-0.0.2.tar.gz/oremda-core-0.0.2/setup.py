# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oremda',
 'oremda.clients',
 'oremda.clients.base',
 'oremda.clients.docker',
 'oremda.clients.singularity',
 'oremda.display',
 'oremda.event_loops',
 'oremda.event_loops.mpi',
 'oremda.messengers',
 'oremda.messengers.base',
 'oremda.messengers.mpi',
 'oremda.messengers.mpi.implementations',
 'oremda.messengers.mqp',
 'oremda.models',
 'oremda.pipeline',
 'oremda.typing',
 'oremda.utils']

package_data = \
{'': ['*']}

install_requires = \
['docker>=5.0.3,<6.0.0',
 'fastapi>=0.73.0,<0.74.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.1,<2.0.0',
 'posix-ipc>=1.0.5,<2.0.0',
 'pyarrow>=6.0.1,<7.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'spython>=0.1.18,<0.2.0']

setup_kwargs = {
    'name': 'oremda-core',
    'version': '0.0.2',
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
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
