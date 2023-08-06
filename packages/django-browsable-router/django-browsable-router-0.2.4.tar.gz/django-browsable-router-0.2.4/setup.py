# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['browsable_router']

package_data = \
{'': ['*']}

install_requires = \
['Django>=1.10', 'djangorestframework>=3.7.0']

extras_require = \
{'typing': ['typing-extensions>=4.0']}

setup_kwargs = {
    'name': 'django-browsable-router',
    'version': '0.2.4',
    'description': 'A Django REST Framework router that can show APIViews and include other routers as navigable urls in the root view.',
    'long_description': '# Django Browsable Router\n\n[![Coverage Status][coverage-badge]][coverage]\n[![GitHub Workflow Status][status-badge]][status]\n[![PyPI][pypi-badge]][pypi]\n[![GitHub][licence-badge]][licence]\n[![GitHub Last Commit][repo-badge]][repo]\n[![GitHub Issues][issues-badge]][issues]\n[![Python Version][version-badge]][pypi]\n\n```shell\npip install django-browsable-router\n```\n\n---\n\n**Documentation**: [https://mrthearman.github.io/django-browsable-router/](https://mrthearman.github.io/django-browsable-router/)\n\n**Source Code**: [https://github.com/MrThearMan/django-browsable-router/](https://github.com/MrThearMan/django-browsable-router/)\n\n---\n\n[coverage-badge]: https://coveralls.io/repos/github/MrThearMan/django-browsable-router/badge.svg?branch=main\n[status-badge]: https://img.shields.io/github/workflow/status/MrThearMan/django-browsable-router/Tests\n[pypi-badge]: https://img.shields.io/pypi/v/django-browsable-router\n[licence-badge]: https://img.shields.io/github/license/MrThearMan/django-browsable-router\n[repo-badge]: https://img.shields.io/github/last-commit/MrThearMan/django-browsable-router\n[issues-badge]: https://img.shields.io/github/issues-raw/MrThearMan/django-browsable-router\n[version-badge]: https://img.shields.io/pypi/pyversions/django-browsable-router\n\n[coverage]: https://coveralls.io/github/MrThearMan/django-browsable-router?branch=main\n[status]: https://github.com/MrThearMan/django-browsable-router/actions/workflows/main.yml\n[pypi]: https://pypi.org/project/django-browsable-router\n[licence]: https://github.com/MrThearMan/django-browsable-router/blob/main/LICENSE\n[repo]: https://github.com/MrThearMan/django-browsable-router/commits/main\n[issues]: https://github.com/MrThearMan/django-browsable-router/issues\n',
    'author': 'Matti Lamppu',
    'author_email': 'lamppu.matti.akseli@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MrThearMan/django-browsable-router',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
