# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['firebasil']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0']

setup_kwargs = {
    'name': 'firebasil',
    'version': '0.1.2',
    'description': 'A modern async Firebase library',
    'long_description': "# firebasil\n\n[![CI](https://github.com/k2bd/firebasil/actions/workflows/ci.yml/badge.svg)](https://github.com/k2bd/firebasil/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/k2bd/firebasil/branch/main/graph/badge.svg?token=0X48PIN0MC)](https://codecov.io/gh/k2bd/firebasil)\n[![PyPI](https://img.shields.io/pypi/v/firebasil)](https://pypi.org/project/firebasil/)\n\nA modern async Firebase library.\n\nDocs TBD\n\n## Developing\n\nInstall [Poetry](https://python-poetry.org/) and `poetry install` the project\n\nInstall the [Firebase CLI](https://firebase.google.com/docs/cli). Make sure the emulators are installed and configured with `firebase init emulators`.\n\n### Useful Commands\n\nNote: if Poetry is managing a virtual environment for you, you may need to use `poetry run poe` instead of `poe`\n\n- `poe autoformat` - Autoformat code\n- `poe lint` - Linting\n- `poe test` - Run Tests\n\n### Release\n\nRelease a new version by manually running the release action on GitHub with a 'major', 'minor', or 'patch' version bump selected.\nThis will create an push a new semver tag of the format `v1.2.3`.\n\nPushing this tag will trigger an action to release a new version of your library to PyPI.\n\nOptionally create a release from this new tag to let users know what changed.\n",
    'author': 'Kevin Duff',
    'author_email': 'kevinkelduff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/k2bd/firebasil',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
