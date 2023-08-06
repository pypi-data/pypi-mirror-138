# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toucan_data_sdk',
 'toucan_data_sdk.fakir',
 'toucan_data_sdk.utils',
 'toucan_data_sdk.utils.generic',
 'toucan_data_sdk.utils.postprocess']

package_data = \
{'': ['*']}

install_requires = \
['engarde>=0.4.0,<0.5.0',
 'joblib<1',
 'pandas>=1.4.1,<2.0.0',
 'python-slugify>=5.0.2,<6.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'toucan-client>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'toucan-data-sdk',
    'version': '7.5.0',
    'description': 'Toucan data SDK',
    'long_description': "[![Pypi-v](https://img.shields.io/pypi/v/toucan-data-sdk.svg)](https://pypi.python.org/pypi/toucan-data-sdk)\n[![Pypi-pyversions](https://img.shields.io/pypi/pyversions/toucan-data-sdk.svg)](https://pypi.python.org/pypi/toucan-data-sdk)\n[![Pypi-l](https://img.shields.io/pypi/l/toucan-data-sdk.svg)](https://pypi.python.org/pypi/toucan-data-sdk)\n[![Pypi-wheel](https://img.shields.io/pypi/wheel/toucan-data-sdk.svg)](https://pypi.python.org/pypi/toucan-data-sdk)\n[![GitHub Actions](https://github.com/ToucanToco/toucan-data-sdk/workflows/CI/badge.svg)](https://github.com/ToucanToco/toucan-data-sdk/actions?query=workflow%3ACI)\n[![codecov](https://codecov.io/gh/ToucanToco/toucan-data-sdk/branch/master/graph/badge.svg?token=GtzvxpgQM9)](https://codecov.io/gh/ToucanToco/toucan-data-sdk)\n# Toucan Data SDK\n\nDevelop your Toucan Toco data pipeline from the confort of your favorite environment.\n\n# Installation\n\nFor usage: `pip install toucan_data_sdk`\n\nFor dev:\n\nInstall the module in editable mode and with test requirements: `pip install -e '.[test]'`\n\n# Usage\n\n## Get data sources\n\n```python\nimport getpass\nfrom toucan_data_sdk import ToucanDataSdk\n\ninstance_url = 'https://api-demo.toucantoco.com'\nauth = ('<username>', getpass.getpass())\n\nsdk = ToucanDataSdk(instance_url, small_app='demo', auth=auth, enable_cache=True)\ndfs = sdk.get_dfs()\n```\n\n# API\n\n## ToucanDataSdk class\n\n### ToucanDataSdk.sdk\n\n* property,\n* uses the client to send a request to the back end to send the data sources\nas DataFrames,\n* uses an internal cache.\n\n### ToucanDataSdk.invalidate_cache()\n\nInvalidates the cache. Next time you will access to the sdk property, a\nrequest will be sent to the client.\n\n### Utils\n\ncf. https://docs.toucantoco.com/concepteur/data-sources/00-generalities.html#utility-functions\n\nFor example:\n\n```python\nfrom toucan_data_sdk.utils import add_missing_row\n```\n\n# Development\n\n## Makefile\n\nUse the makefile to `test`, `build`...\n\n```shell\n$ make test\n```\n\n# Development\n\nYou need to install [poetry](https://python-poetry.org/) either globally or in a virtualenv.\nThen run `make install`\n",
    'author': 'Toucan Toco',
    'author_email': 'dev@toucantoco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ToucanToco/toucan-data-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
