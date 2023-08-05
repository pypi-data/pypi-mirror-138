# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['command_log',
 'command_log.management.commands',
 'command_log.migrations',
 'command_log.utils']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<5.0']

setup_kwargs = {
    'name': 'django-command-log',
    'version': '1.0',
    'description': 'Django management command auditing app',
    'long_description': '# Django Management Command Log\n\nApp to enable simple auditing of Django management commands\n\n### Version support\n\nThis project now support Django 2.2+, and Python 3.7+.\nSee git tags and PyPI classifiers for support.\n\n## Background\n\nThis app wraps the standad Django management command base class to record the\nrunning of a command. It logs the name of the command, start and end time, and\nthe output (if any). If the command fails with a Python exception, the error\nmessage is added to the record, and the exception itself is logged using\n`logging.exception`.\n\n![Screenshot of admin list\nview](https://github.com/yunojuno/django-management-command-log/blob/master/screenshots/list-view.png)\n\n![Screenshot of admin detail\nview](https://github.com/yunojuno/django-management-command-log/blob/master/screenshots/detail-view.png)\n\nSee the `test_command` and `test_transaction_command` for examples.\n\n## TODO\n\n* Documentation.\n* Convert output field to JSON\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yunojuno/django-management-command-log',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
