# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src',
 'src.blog',
 'src.builder',
 'src.converters',
 'src.dataclasses',
 'src.entities',
 'src.lib',
 'src.obsidian',
 'src.preprocessors',
 'src.tasks',
 'src.tree']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.6,<4.0.0',
 'docopt>=0.6.2,<0.7.0',
 'markdown-link-attr-modifier>=0.2.0,<0.3.0',
 'pybars4>=0.9.13,<0.10.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'python-frontmatter>=1.0.0,<2.0.0',
 'python-slugify>=5.0.2,<6.0.0',
 'watchdog>=2.1.6,<3.0.0']

setup_kwargs = {
    'name': 'obsidian-blog',
    'version': '0.1.0',
    'description': 'Feature rich static site generator for obsidian.md',
    'long_description': None,
    'author': "'Anton Shuvalov'",
    'author_email': 'anton@shuvalov.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
