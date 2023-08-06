# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semmy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'semmy',
    'version': '0.2.0',
    'description': 'Semantic versioning made easy for Python',
    'long_description': '<h1>Semmy</h1>\n\n> Semantic versioning made easy for Python\n\n* [Features](#features)\n* [API](#api)\n* [Prerequisites](#prerequisites)\n* [Install](#install)\n* [Contributing](#contributing)\n\n## Features\n\n* Parses semantic version domain objects from valid strings\n* Check if two versions are equal\n* Check if version is a pre-release\n* Check if version is are greater/less (upcoming)\n* Bump versions according to different strategies (upcoming)\n\n## API\n\nTo be written.\n\nCheck [unit tests](tests/test_semmy.py) for complete examples.\n\n## Prerequisites\n\n* **Python** >=3.8 or later\n\n## Install\n\n```sh\npoetry add semmy\n```\n\nAlternatively, for older projects.\n\n```sh\npip install semmy\npip freeze > requirements.txt\n```\n\n## Contributing\n\nSee [**here**](CONTRIBUTING.md) for instructions.\n',
    'author': 'Niko Heikkilä',
    'author_email': 'yo@nikoheikkila.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/semmy/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
