# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classy_config', 'classy_config.loader']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0',
 'pyright>=0.0.13,<0.0.14',
 'toml>=0.10.2,<0.11.0',
 'typing-inspect>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'classy-config',
    'version': '0.2.0a3',
    'description': 'ClassyConfig is a Python3 package aiming to remove the need for a config.py or settings.py file.',
    'long_description': '# ClassyConfig\n\n`ClassyConfig` is a Python3 package aiming to remove the need for a `config.py` or `settings.py` file.\n\n```py\n\nfrom classy_config import BaseModel, ConfigValue, register_config\n\n# Create your global config manager (example test-config.json below)\nregister_config(filepath="config.toml")\n\n\n# Resolve default values based on your config\ndef print_current_version(version: str = ConfigValue("package", str)) -> None:\n    print(version)\n\n\n# Use Pydantic Models for your config\nclass Author(BaseModel):\n    username: str\n    email: str\n    lucky_number: int\n\n\n# Resolve default values based on your config\ndef print_author(author: Author = ConfigValue("author", Author)) -> None:\n    print(author)\n\n\n# Allows for nested values\ndef print_value(value: int = ConfigValue("nested.value", int)) -> None:\n    print(value)\n```\n\n```toml\npackage="ClassyConfig"\n\n[author]\nusername="GDWR"\nemail="gregory.dwr@gmail.com"\nlucky_number=17\n\n[nested]\nvalue=10\n```\n',
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
