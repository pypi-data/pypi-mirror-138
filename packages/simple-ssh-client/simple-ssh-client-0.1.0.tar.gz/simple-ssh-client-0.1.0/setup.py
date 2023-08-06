# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ssh_client']
install_requires = \
['paramiko>=2.9.2,<3.0.0', 'pydantic>=1.9.0,<2.0.0', 'retry>=0.9.2,<0.10.0']

setup_kwargs = {
    'name': 'simple-ssh-client',
    'version': '0.1.0',
    'description': 'Simple SSH client based on Paramiko',
    'long_description': '',
    'author': 'Wojciech Richert',
    'author_email': '33549959+wojtekrichert@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wojtekrichert/simple-ssh-client',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
