# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['attribute']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'attribute',
    'version': '0.1.4',
    'description': 'Attribute management made easy',
    'long_description': "# attribute\nAttribute management made easy\n\n## Installation\n```console\npip install git+https://github.com/tombulled/attribute@main\n```\n\n## Usage\n```python\n>>> import attribute\n>>>\n>>> def foo(): pass\n>>>\n>>> name = attribute.Attribute('__name__')\n>>>\n>>> name.get(foo)\n'foo'\n```",
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tombulled/attribute',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
