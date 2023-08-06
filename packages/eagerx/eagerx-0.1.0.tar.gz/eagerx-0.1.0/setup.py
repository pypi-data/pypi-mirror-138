# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eagerx',
 'eagerx.bridges',
 'eagerx.bridges.ode',
 'eagerx.bridges.openai_gym',
 'eagerx.bridges.real',
 'eagerx.bridges.test',
 'eagerx.converters',
 'eagerx.core',
 'eagerx.enginestates',
 'eagerx.nodes',
 'eagerx.utils',
 'eagerx.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Rx>=3.2.0,<4.0.0',
 'defusedxml>=0.7.1,<0.8.0',
 'gym>=0.21.0,<0.22.0',
 'netifaces>=0.11.0,<0.12.0',
 'networkx>=2.5.1,<3.0.0',
 'opencv-python>=4.3.0.36,<5.0.0.0',
 'psutil>=5.9.0,<6.0.0',
 'rospkg>=1.3.0,<2.0.0',
 'scikit-image>=0.17.2,<0.18.0',
 'scipy>=1.5.4,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'eagerx',
    'version': '0.1.0',
    'description': 'Engine Angostic Gym Environments for Robotics',
    'long_description': None,
    'author': 'Bas van der Heijden',
    'author_email': 'd.s.vanderheijden@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
