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
    'version': '0.6.0',
    'description': 'Network Automation and Programmability Abstraction Layer with Multivendor support for PANOS.',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/napalm-panos.svg)](https://pypi.python.org/pypi/napalm-panos)\n[![PyPI](https://img.shields.io/pypi/dm/napalm-panos.svg)](https://pypi.python.org/pypi/napalm-panos)\n[![Build Status](https://travis-ci.org/napalm-automation/napalm-panos.svg?branch=master)](https://travis-ci.org/napalm-automation/napalm-panos)\n[![Coverage Status](https://coveralls.io/repos/github/napalm-automation/napalm-panos/badge.svg?branch=develop)](https://coveralls.io/github/napalm-automation/napalm-panos?branch=develop)\n\n# NAPALM PANOS\n\nThis is community version of [NAPALM](https://napalm.readthedocs.io/) for the Palo Alto firewall operating system. For standard tutorials and overview of NAPALM, please review their documentation.\n\n# Configuration Support\n\nThis table identifies the currently available configuration methods supported:\n\n| Getter                    | Supported |\n| ------------------------- | --------- |\n| Config Replace            | ✅        |\n| Commit Confirm            | ❌        |\n| Config Merge              | ✅        |\n| Compare Config            | ✅        |\n| Atomic Changes            | ✅        |\n| Rollback                  | ✅        |\n\n> Commit Confirm is not supported by the vendor at the time of this writing.\n\nConfiguration Lock is also supported, but the `optional_args` `config_lock` key set to `True`. You can see in this example.\n\n```\nfrom napalm import get_network_driver\n\npanos_device = device"\npanos_user = "admin"\npanos_password = "pass123"\ndriver = get_network_driver("panos")\noptional_args = {"config_lock": True}\n\nwith driver(panos_device, panos_user, panos_password, optional_args=optional_args) as device:\n    device.load_replace_candidate(filename="2022-01-01-intended-config.xml")\n    device.commit_config()\n```\n\nAs shown in the example above, the use of NAPALM\'s context manager is supported and recommended to use. \n\nThe locks are acquired and released using XML API. Locks for config and commit lock are obtained and released separately from each other. Both locks are\nreleased automatically by the device when a commit is made on the device.\n\nFor troubleshooting:\n- The code crashed in a way that the lock could not be removed?\n    - Remove the lock manually (CLI, API, Web UI). The lock can only be removed by the administrator who set it, or by a superuser.\n- The lock disappeared in the middle of program execution?\n    - Did someone do a commit on the device? The locks are removed automatically when the administrator who set the locks performs a commit operation on the device.\n\n# Supported Getters\n\nThis table identifies the currently available getters and the support for each:\n\n| Getter                    | Supported |\n| ------------------------- | --------- |\n| get_arp_table             | ✅        |\n| get_bgp_config            | ❌        |\n| get_bgp_neighbors         | ❌        |\n| get_bgp_neighbors_detail  | ❌        |\n| get_config                | ✅        |\n| get_environment           | ❌        |\n| get_facts                 | ✅        |\n| get_firewall_policies     | ❌        |\n| get_interfaces            | ✅        |\n| get_interfaces_counters   | ❌        |\n| get_interfaces_ip         | ✅        |\n| get_ipv6_neighbors_table  | ❌        |\n| get_lldp_neighbors        | ✅        |\n| get_lldp_neighbors_detail | ❌        |\n| get_mac_address_table     | ❌        |\n| get_network_instances     | ❌        |\n| get_ntp_peers             | ❌        |\n| get_ntp_servers           | ❌        |\n| get_ntp_stats             | ❌        |\n| get_optics                | ❌        |\n| get_probes_config         | ❌        |\n| get_probes_results        | ❌        |\n| get_route_to              | ✅        |\n| get_snmp_information      | ❌        |\n| get_users                 | ❌        |\n| get_vlans                 | ❌        |\n| is_alive                  | ✅        |\n| ping                      | ❌        |\n| traceroute                | ❌        |\n',
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
