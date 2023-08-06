# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_cookiecutter_template',
 'poetry_cookiecutter_template.src.core',
 'poetry_cookiecutter_template.src.tests.unit',
 'poetry_cookiecutter_template.src.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poetry-cookiecutter-template',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'whc',
    'author_email': '249768447@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
