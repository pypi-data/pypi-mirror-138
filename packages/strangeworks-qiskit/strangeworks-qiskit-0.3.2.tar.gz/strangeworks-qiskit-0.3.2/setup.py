# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strangeworks',
 'strangeworks.qiskit',
 'strangeworks.qiskit.backends',
 'strangeworks.qiskit.jobs']

package_data = \
{'': ['*']}

install_requires = \
['qiskit-aer==0.10.3',
 'qiskit-ibmq-provider==0.18.3',
 'qiskit-terra==0.19.2',
 'qiskit==0.34.2',
 'strangeworks>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'strangeworks-qiskit',
    'version': '0.3.2',
    'description': 'Strangeworks Qiskit SDK Extension',
    'long_description': '| ⚠️    | This SDK is currently in pre-release alpha state and subject to change. To get more info or access to test features check out the [Strangeworks Backstage Pass Program](https://strangeworks.com/backstage). |\n|---------------|:------------------------|\n\n# Strangeworks Qiskit Extension\n\nStrangeworks Python SDK extension for Qiskit. \n\n\n \nFor more information on using the SDK check out the [Strangeworks documentation](https://docs.strangeworks.com/).\n',
    'author': 'Strange Devs',
    'author_email': 'hello@strangeworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
