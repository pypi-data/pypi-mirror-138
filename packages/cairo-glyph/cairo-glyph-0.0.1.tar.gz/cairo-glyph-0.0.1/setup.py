# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glyph']

package_data = \
{'': ['*']}

modules = \
['.keep']
install_requires = \
['typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['glyph = glyph.main:app']}

setup_kwargs = {
    'name': 'cairo-glyph',
    'version': '0.0.1',
    'description': 'A package manager for Cairo contracts',
    'long_description': '# glyph\n\nA proof-of-concept package manager for Cairo contracts/libraries. Distribution through pypi. Installation through existing package managers -- pip, pipenv, poetry.\n\nIntended to be a lightweight layer on top of existing python package management. Sole responsibility is collecting contracts/libraries registered to the `contracts` [namespace package](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-namespace-packages), and copying their contents to a new `contracts/lib` folder.\n\n## Usage\n\n```\n$ glyph --help\nUsage: glyph [OPTIONS] COMMAND [ARGS]...\n\n  A proof-of-concept package manager for Cairo.\n\nOptions:\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n  --help                Show this message and exit.\n\nCommands:\n  clean  Remove everything in the lib directory\n  use    Install one or all added cairo packages in the project\n```\n\nUse all libraries installed to the venv:\n```\n$ glyph use --all\n🔎 Discovering installed contracts...\n\n • Using contracts.placeholder\n\n✅ Done.\n```\n\n> TODO: add real example from pypi\n\n\n## Library Setup\n\nIn order to allow your contracts to be installed, a few conventions must be followed.\n\n```\ncontracts                # The "namespace package" that the contracts are installed to\n└── placeholder          # The library you are distributing\n    ├── contract.cairo\n    └── __init__.py      # Required to be installable.\nsetup.py                 # The installer\n```\n\nThe actual `setup.py` will look something like this:\n\n```python\nfrom setuptools import setup\n\n\nsetup(\n    name="placeholder",\n\n    version="1",\n    description="",\n    long_description="",\n\n    author="Jane Doe",\n    author_email="author@example.com",\n\n    license="MIT License",\n\n    packages=["contracts.placeholder"],\n    # Include all extra package data. Possible to include *.cairo only\n    package_data={"": ["*"]},\n    zip_safe=False,\n)\n```\n\nOnce distributed on pypi, one could:\n```\n(venv) $ pip install cairo-glyph cairo-placeholder\n...\n(venv) $ glyph use placeholder\n🔎 Discovering installed contracts...\n\n • Using contracts.placeholder\n\n✅ Done.\n```\n\nAdding the following to your project:\n```\ncontracts/\n└── libs\n    └── placeholder\n        └── contract.cairo\n```',
    'author': 'Sam Barnes',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
