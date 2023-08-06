# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['creosote']

package_data = \
{'': ['*']}

install_requires = \
['distlib>=0.3.4,<0.4.0', 'loguru>=0.6.0,<0.7.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['creosote = creosote.cli:main']}

setup_kwargs = {
    'name': 'creosote',
    'version': '1.0.1',
    'description': 'Identify unused dependencies and avoid a bloated virtual environment.',
    'long_description': '# creosote\n\n[![check](https://github.com/fredrikaverpil/creosote/actions/workflows/check.yaml/badge.svg)](https://github.com/fredrikaverpil/creosote/actions/workflows/check.yaml) [![test](https://github.com/fredrikaverpil/creosote/actions/workflows/test.yaml/badge.svg)](https://github.com/fredrikaverpil/creosote/actions/workflows/test.yaml)\n\nIdentify unused dependencies and avoid a bloated virtual environment.\n\n## Quickstart\n\nInstall creosote in separate virtual environment (using e.g. [pipx](https://github.com/pypa/pipx)):\n\n```bash\npipx install creosote\n```\n\nScan virtual environment for unused packages:\n\n```bash\ncreosote --deps-file pyproject.toml --venv .venv --paths src\n```\n\nExample output:\n\n```bash\n$ creosote\nParsing src/creosote/formatters.py\nParsing src/creosote/models.py\nParsing src/creosote/resolvers.py\nParsing src/creosote/__init__.py\nParsing src/creosote/parsers.py\nParsing src/creosote/cli.py\nParsing pyproject.toml for packages\nFound packages in pyproject.toml: PyYAML, distlib, loguru, protobuf, toml\nResolving...\nUnused packages found: PyYAML, protobuf\n```\n\nGet help:\n\n```bash\ncreosote --help\n```\n\n## How this works\n\nSome data is required as input:\n\n- A list of package names (fetched from e.g. `pyproject.toml`, `requirements_*.txt|.in`)\n- The path to the virtual environment\n- The path to one or more Python files\n\nThe creosote tool will first scan the given python file(s) for all its imports. Then it fetches all package names. Finally, all imports are associated with their corresponding package name. If a package does not have any imports associated, it will be considered to be unused.\n\n## Ambition and history\n\nThe idea of a package like this was born from having gotten security vulnerability\nreports about production dependencies (shipped into production) which turned out to not not\neven be in use.\n\nThe goal would be to be able to run this tool in CI, which will catch cases where the developer\nforgets to remove unused packages. A example of such a case could be when doing refactorings.\n\nThis can work well in tandem with flake8 or pylint, which can warn in CI about unused imports.\n\nNote: The creosote tool supports identifying both unused production dependencies and developer dependencies.\n\n## FAQ\n\n### Are requirements.txt files supported?\n\nYes, kind of. There is no way to tell which part of `requirements.txt` specifies production vs developer dependencies. Therefore, you have to break your `requirements.txt` file into e.g. `requirements-prod.txt` and `requirements-dev.txt` and use any of them as input.\n\nIf you are using [pip-tools](https://github.com/jazzband/pip-tools), you can provide a `*.in` file.\n\n### Can I scan for pyproject\'s dev-dependencies?\n\nYes! For `pyproject.toml`, just provide the `--dev` argument.\n\n### Can I use this as a GitHub Action?\n\nYes! See [.github/workflows/action.yaml](.github/workflows/action.yaml) for a working example.\n\n### What\'s with the name "creosote"?\n\nThis library has borrowed its name from the [Monty Python scene about Mr. Creosote](https://www.youtube.com/watch?v=aczPDGC3f8U).\n',
    'author': 'Fredrik Averpil',
    'author_email': 'fredrik.averpil@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fredrikaverpil/creosote',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
