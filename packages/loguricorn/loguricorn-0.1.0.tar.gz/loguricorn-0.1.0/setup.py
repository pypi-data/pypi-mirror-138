# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loguricorn']

package_data = \
{'': ['*']}

install_requires = \
['gunicorn>=20.1.0,<21.0.0', 'loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'loguricorn',
    'version': '0.1.0',
    'description': 'A small package for rerouting gunicorn logs to loguru',
    'long_description': '# loguricorn\n\n<p align="center">\n    <a href="https://github.com/jmgilman/loguricorn/actions/workflows/ci.yml">\n        <img src="https://github.com/jmgilman/loguricorn/actions/workflows/ci.yml/badge.svg"/>\n    </a>\n    <a href="https://pypi.org/project/loguricorn">\n        <img src="https://img.shields.io/pypi/v/loguricorn"/>\n    </a>\n</p>\n\n> A small package for rerouting [gunicorn][1] logs to [loguru][2]\n\n![Example](example.svg)\n\nThis package provides a compatible interface for automatically routing\n`gunicorn` logs to the popular `loguru` library.\n\n## Usage\n\nInstall the package:\n\n```shell\npip install loguricorn\n```\n\nThen pass the custom interface to gunicorn at runtime:\n\n```shell\ngunicorn --logger-class loguricorn.Logger tests.app:app\n```\n\nAll log records will now be routed through the default `loguru.logger`.\n\n## Configuration\n\nIt\'s possible to customize the `loguru.logger` instance before `gunicorn`\ninitializes itself. Simply add your changes in a configuration file and pass it\nto gunicorn at runtime:\n\n```python\nimport sys\n\nfrom loguru import logger\n\nlogger.remove()\nlogger.add(\n    sys.stderr,\n    colorize=True,\n    format="<green>{time}</green> <level>{message}</level>",\n)\n```\n\n```shell\ngunicorn -c conf.py --logger-class loguricorn.Logger tests.app:app\n```\n\nIt\'s recommended to import any customizations from your main application and\nuse them in the configuration in order to obtain a consistent log record format\nacross the entire execution.\n\n## Testing\n\nTesting is done by starting `gunicorn` in a subprocess with the custom logger\nenabled and validating that the emitted logs match the expected format.\n\nInstall dev dependencies:\n\n```shell\npoetry install\n```\n\nRun test:\n\n```shell\npoetry run tox .\n```\n\n## Contributing\n\nCheck out the [issues][3] for items needing attention or submit your own and\nthen:\n\n1. [Fork the repo][4]\n2. Create your feature branch (git checkout -b feature/fooBar)\n3. Commit your changes (git commit -am \'Add some fooBar\')\n4. Push to the branch (git push origin feature/fooBar)\n5. Create a new Pull Request\n\n[1]: https://github.com/Delgan/loguru\n[2]: https://github.com/benoitc/gunicorn\n[3]: https://github.com/jmgilman/loguricorn/issues\n[4]: https://github.com/jmgilman/loguricorn/fork\n',
    'author': 'Joshua Gilman',
    'author_email': 'joshuagilman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmgilman/loguricorn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
