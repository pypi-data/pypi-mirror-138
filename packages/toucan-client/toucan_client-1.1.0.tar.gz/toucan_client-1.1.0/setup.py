# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toucan_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'toucan-client',
    'version': '1.1.0',
    'description': 'Toucan API client',
    'long_description': "[![Pypi-v](https://img.shields.io/pypi/v/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)\n[![Pypi-pyversions](https://img.shields.io/pypi/pyversions/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)\n[![Pypi-l](https://img.shields.io/pypi/l/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)\n[![Pypi-wheel](https://img.shields.io/pypi/wheel/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)\n[![GitHub Actions](https://github.com/ToucanToco/toucan-client/workflows/CI/badge.svg)](https://github.com/ToucanToco/toucan-client/actions?query=workflow%3ACI)\n[![codecov](https://codecov.io/gh/ToucanToco/toucan-client/branch/main/graph/badge.svg)](https://codecov.io/gh/ToucanToco/toucan-client)\n\n# Installation\n\n`pip install toucan_client`\n\n# Usage\n\n```python\n# Initialize client\nauth = ('<username>', '<password>')\nclient = ToucanClient('https://api.some.project.com/my_small_app', auth=auth)\n\n# Retrieve ETL config\netl_config = client.config.etl.get()  # -> GET 'https://api.some.project.com/config/etl'\nclient.config.etl.get(stage='staging')  # -> GET 'https://api.some.project.com/config/etl?stage=staging'\n\n# Operations control, start a preprocess\nclient.data.preprocess.post(stage='staging', json={'async': True})\n\n# Operations control, release to prod\nclient.data.release.post(stage='staging')\n```\n\n# Development\n\nYou need to install [poetry](https://python-poetry.org/) either globally or in a virtualenv.\nThen run `make install`\n",
    'author': 'Toucan Toco',
    'author_email': 'dev@toucantoco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ToucanToco/toucan-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
