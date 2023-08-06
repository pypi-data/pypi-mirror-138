# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluentstream']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fluentstream',
    'version': '0.1.0',
    'description': 'A stream abstraction with a fluent interface. Inspired by Java 8 streams.',
    'long_description': '# Fluent stream\n \nA stream abstraction with a fluent interface. Inspired by Java 8 streams, but a lot simpler and not lazy. \nIt allows you to express something like: \n\n```python\nStream([1, 2, 3, 4, 5, 6, 7, 8, 9])\\\n    .filter(lambda x: x % 2 == 0)\\\n    .map(lambda x: x + 0.5)\\\n    .limit(4)\\\n    .fold(lambda x, y: x + y)\n```',
    'author': 'Mikael M',
    'author_email': 'binarybusiness@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/binarybusiness/fluentstream.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
