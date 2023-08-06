# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_publish_amash']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypi-publish-amash',
    'version': '0.1',
    'description': 'Empty package to test the GitHub Action `coveooss/pypi-publish-with-poetry`',
    'long_description': 'This package is used to validate the functionality of the "coveooss/pypi-publish-with-poetry" GitHub action.\n\nYou can read more about the action [here](https://github.com/coveooss/pypi-publish-with-poetry).\n',
    'author': 'Jonathan Piché',
    'author_email': 'tools@coveo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iaanimashaun/pypi-publish.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
