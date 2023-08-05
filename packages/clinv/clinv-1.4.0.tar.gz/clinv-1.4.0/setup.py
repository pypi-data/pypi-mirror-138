# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['clinv', 'clinv.adapters', 'clinv.entrypoints', 'clinv.model']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.20.24,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'goodconf[yaml]>=2.0.1,<3.0.0',
 'repository-orm>=0.7.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.16.0,<11.0.0']

entry_points = \
{'console_scripts': ['autodev = autodev.entrypoints.cli:cli',
                     'clinv = clinv.entrypoints.cli:cli']}

setup_kwargs = {
    'name': 'clinv',
    'version': '1.4.0',
    'description': 'DevSecOps command line asset inventory',
    'long_description': '# Clinv\n\n[![Actions Status](https://github.com/lyz-code/clinv/workflows/Tests/badge.svg)](https://github.com/lyz-code/clinv/actions)\n[![Actions Status](https://github.com/lyz-code/clinv/workflows/Build/badge.svg)](https://github.com/lyz-code/clinv/actions)\n[![Coverage Status](https://coveralls.io/repos/github/lyz-code/clinv/badge.svg?branch=master)](https://coveralls.io/github/lyz-code/clinv?branch=master)\n\nDevSecOps command line asset inventory\n\n## Help\n\nSee [documentation](https://lyz-code.github.io/clinv) for more details.\n\n## Installing\n\n```bash\npip install clinv\n```\n\n## Contributing\n\nFor guidance on setting up a development environment, and how to make\na contribution to *clinv*, see [Contributing to\nclinv](https://lyz-code.github.io/clinv/contributing).\n\n## License\n\nGPLv3\n',
    'author': 'Lyz',
    'author_email': 'lyz-code-security-advisories@riseup.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lyz-code/clinv',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<=3.10',
}


setup(**setup_kwargs)
