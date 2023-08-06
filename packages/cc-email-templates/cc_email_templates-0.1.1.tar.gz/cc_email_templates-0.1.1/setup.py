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
    'version': '0.1.1',
    'description': 'A set of email templates used by Conflict Cartographer',
    'long_description': '\n# Conflict Cartographer Email Templates\n\nThis package contains email templates packages as Jinja2 templates, exposed via\na set of functions.\n\n## Installation\n\n```\npip install cc-email-templates\n```\n\n## Usage\n\n```\nimport cc_email_templates \n\nemail_txt, email_html = cc_email_templates.call_to_action_email(\n      title = "My call to action",\n      content_above = "Please click my link",\n      action_button_text = "Link",\n      action_link = "http://www.example.com"\n   )\n\nsend_email(..., html_content = email_html, content = email_txt)\n```\n\n## Credits\n\nBase template was "forked" and adapted from [this repo](https://github.com/leemunroe/responsive-html-email-template)\n',
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/prio-data/cc_email_templates',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
