# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ytcomment_trends',
 'ytcomment_trends.controllers.google_api',
 'ytcomment_trends.controllers.nlp']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=2.36.0,<3.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'oseti>=0.2,<0.3',
 'pandas>=1.3.5,<2.0.0']

entry_points = \
{'console_scripts': ['ytcomment_trends = '
                     'ytcomment_trends.entrypoint:entrypoint']}

setup_kwargs = {
    'name': 'ytcomment-trends',
    'version': '0.1.7',
    'description': 'YouTube comment trends analysis tool using oseti',
    'long_description': "# ytcomment_trends\n\n[![PyPI version](https://badge.fury.io/py/ytcomment-trends.svg)](https://badge.fury.io/py/ytcomment-trends)\n\n[![Python Versions](https://img.shields.io/pypi/pyversions/ytcomment-trends.svg)](https://pypi.org/project/ytcomment-trends/)\n\n## Dependencies\n\nBefore install this library, you need to install mecab for NLP.\n\nFor macOS, run this command to install mecab and ipadic dictionary. For other OS, please follow the instructions from mecab official documentation.\n\n```\nbrew install mecab mecab-ipadic\n```\n\n## How to use\n\n### Get YouTube API Client Secret\n\nPlease refer to [Google's official documentation](https://developers.google.com/youtube/registering_an_application) for getting API keys. Make sure you create credentials with API Key (not OAuth 2.0 Client) with API restriction to the YouTube Data API.\n\n### Run command\n\nInstall this library with the following command:\n\n```\npip install ytcomment_trends\n```\n\nIf you are using virtual environment, please use the package manager of the virtual environment (e.g., `pipenv install`, `poetry add`).\n\nAfter installation, run this command to analyze video.\n\n```\nytcomment_trends -v pR2E2OatMTQ -k hogefuga\n```\n\nIf you are not sure about the arguments, run following command to check.\n\n```\nytcomment_trends -h\n```",
    'author': 'Kyosuke Miyamura',
    'author_email': 'ask@386.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.386.jp/works/ytcomment_trends',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
