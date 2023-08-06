# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classy_config', 'classy_config.parser']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0',
 'pyright>=0.0.13,<0.0.14',
 'typing-inspect>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'classy-config',
    'version': '0.2.0a0',
    'description': 'ClassyConfig is a Python3 package aiming to remove the need for a config.py or settings.py file.',
    'long_description': '# ClassyConfig\n\n`ClassyConfig` is a Python3 package aiming to remove the need for a `config.py` or `settings.py` file.\n\n```py\n\nfrom classy_config import BaseModel, ClassyConfig, ConfigParam\n\n# Create your global config manager (example test-config.json below)\nconfig = ClassyConfig(config_file="test-config.json")\n\n# Resolve default values based on your config\ndef print_current_version(version: str = ConfigParam("version", str)) -> None:\n    print(version)\n\n# Use Pydantic Models for your config\nclass Author(BaseModel):\n    username: str\n    email: str\n    lucky_number: int\n\n# Resolve default values based on your config\ndef print_author(author: Author = ConfigParam("author", Author)) -> None:\n    print(author)\n    \n# Allows for nested values\ndef print_value(value: int = ConfigParam("nested.value", int)) -> None:\n    print(value)\n```\n```json\n{\n  "version": "0.0.1",\n  \n  "author": {\n    "username": "GDWR",\n    "email": "gregory.dwr@gmail.com",\n    "lucky_number": 17\n  },\n\n  "nested": {\n    "value": 10\n  }\n}\n```\n',
    'author': 'GDWR',
    'author_email': 'gregory.dwr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GDWR/classy-config',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
