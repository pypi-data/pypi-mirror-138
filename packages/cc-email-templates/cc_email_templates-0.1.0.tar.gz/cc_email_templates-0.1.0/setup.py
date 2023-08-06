# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cc_email_templates', 'cc_email_templates.templates']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0', 'css-inline>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'cc-email-templates',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
