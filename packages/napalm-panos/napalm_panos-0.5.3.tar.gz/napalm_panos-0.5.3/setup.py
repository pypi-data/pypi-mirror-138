# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['napalm_panos', 'napalm_panos.utils']

package_data = \
{'': ['*'],
 'napalm_panos': ['templates/*'],
 'napalm_panos.utils': ['textfsm_templates/*']}

install_requires = \
['cryptography==3.3.2',
 'lxml==4.6.5',
 'napalm>=3.0,<4.0',
 'netmiko>=3.3.2,<4.0.0',
 'pan-python',
 'requests-toolbelt',
 'xmltodict']

setup_kwargs = {
    'name': 'napalm-panos',
    'version': '0.5.3',
    'description': 'Network Automation and Programmability Abstraction Layer with Multivendor support for PANOS.',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/napalm-panos.svg)](https://pypi.python.org/pypi/napalm-panos)\n[![PyPI](https://img.shields.io/pypi/dm/napalm-panos.svg)](https://pypi.python.org/pypi/napalm-panos)\n[![Build Status](https://travis-ci.org/napalm-automation/napalm-panos.svg?branch=master)](https://travis-ci.org/napalm-automation/napalm-panos)\n[![Coverage Status](https://coveralls.io/repos/github/napalm-automation/napalm-panos/badge.svg?branch=develop)](https://coveralls.io/github/napalm-automation/napalm-panos?branch=develop)\n\n# napalm-panos\n',
    'author': 'Gabriele Gerbino',
    'author_email': 'gabriele@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/napalm-automation/napalm-panos',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
