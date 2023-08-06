# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['model_pool']

package_data = \
{'': ['*']}

install_requires = \
['icecream>=2.1.1,<3.0.0', 'install>=1.3.5,<2.0.0', 'logzero>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'model-pool',
    'version': '0.1.0',
    'description': 'pack_name descr ',
    'long_description': '# align-model-pool\n[![pytest](https://github.com/ffreemt/align-model-pool/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/align-model-pool/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/model_pool.svg)](https://badge.fury.io/py/model_pool)\n\nVarious alignment models for colab and hf-spaces\n\n## Install it\n\n```shell\npip install model_pool\n# or poetry add model_pool\n# pip install git+htts://github.com/ffreemt/align-model-pool\n# poetry add git+htts://github.com/ffreemt/align-model-pool\n\n# To upgrade\npip install model_pool -U\n# or poetry add model_pool@latest\n```\n\n## Use it\n```python\nimport model_pool\n\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/align-model-pool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0',
}


setup(**setup_kwargs)
