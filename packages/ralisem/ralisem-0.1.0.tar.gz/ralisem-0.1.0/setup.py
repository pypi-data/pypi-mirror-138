# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ralisem']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.5.0,<4.0.0']

extras_require = \
{'dev-all': ['black>=21.11b1,<22.0',
             'isort>=5.10.1,<6.0.0',
             'pre-commit>=2.15.0,<3.0.0',
             'pytest>=6.2.5,<7.0.0',
             'pytest-cov>=3.0.0,<4.0.0',
             'coveralls>=3.3.1,<4.0.0',
             'coverage>=6.1.2,<7.0.0',
             'bumpversion>=0.5.3,<0.6.0',
             'autoflake>=1.4,<2.0',
             'mypy>=0.930,<0.931',
             'mkdocs>=1.2.3,<2.0.0',
             'mkdocs-material>=8.0.2,<9.0.0',
             'mike>=1.1.2,<2.0.0'],
 'dev-check': ['mypy>=0.930,<0.931'],
 'dev-deploy': ['bumpversion>=0.5.3,<0.6.0'],
 'dev-docs': ['mkdocs>=1.2.3,<2.0.0',
              'mkdocs-material>=8.0.2,<9.0.0',
              'mike>=1.1.2,<2.0.0'],
 'dev-style': ['black>=21.11b1,<22.0',
               'isort>=5.10.1,<6.0.0',
               'pre-commit>=2.15.0,<3.0.0',
               'autoflake>=1.4,<2.0'],
 'dev-test': ['pytest>=6.2.5,<7.0.0',
              'pytest-cov>=3.0.0,<4.0.0',
              'coveralls>=3.3.1,<4.0.0',
              'coverage>=6.1.2,<7.0.0']}

setup_kwargs = {
    'name': 'ralisem',
    'version': '0.1.0',
    'description': 'Rate limit semaphore for async-style   (any core)',
    'long_description': '# Rate Limit Semaphore\n> Rate limit semaphore for async-style (any core)\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ralisem)\n![PyPI - Implementation](https://img.shields.io/pypi/implementation/ralisem)\n![PyPI](https://img.shields.io/pypi/v/ralisem)\n[![Coverage Status](https://coveralls.io/repos/github/deknowny/rate-limit-semaphore/badge.svg?branch=main)](https://coveralls.io/github/deknowny/rate-limit-semaphore?branch=main)\n***\nThere are two implementations of rate limit semaphore. Live demo shows how [FixedNewPreviousDelaySemaphore](./examples/new_previous.py) and [FixedNewFirstDelaySemaphore](./examples/new_first.py) work\n***\n![Live demo](./assets/new-previous-live-demo.gif)\n![Live demo](./assets/new-first-live-demo.gif)\n\n\n## Overview\n```python\nimport datetime\nimport ralisem\n\n# Or another implementation\nsem = ralisem.FixedNewPreviousDelaySemaphore(\n    access_times=3, per=datetime.timedelta(seconds=1)\n)\nasync with sem:\n    ...\n```\nDifference:\n* `FixedNewPreviousDelaySemaphore`: Sures the last and a new access have a fixed required delay (`per / access_times`)\n* `FixedNewFirstDelaySemaphore`: Sures first and last in series (serias is `access_times`) have a fixed delay (`per`)\n\n## Methods\nAll of these implementations are inherited from one base `TimeRateLimitSemaphoreBase`. Check out full methods [here](./ralisem/base.py)\n\n# Installation\nVia PyPI:\n```shell\npython -m pip install ralisem\n```\nOr via GitHub\n```shell\npython -m pip install https://github.com/deknowny/rate-limit-semaphore/archive/main.zip\n```\n# Contributing\nCheck out [Contributing section](./CONTRIBUTING.md)\n',
    'author': 'Yan Kurbatov',
    'author_email': 'deknowny@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/deknowny/rate-limit-semaphore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
