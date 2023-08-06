# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gridview']

package_data = \
{'': ['*']}

install_requires = \
['svgwrite>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'gridview',
    'version': '0.1.2',
    'description': 'Visualize your 2D iterable.',
    'long_description': '# GridView\n\nVisualize your 2D iterable. See our usage [examples](https://gergelyk.github.io/python-gridview) now!\n\n* Documentation: <https://gergelyk.github.io/python-gridview>\n* Repository: <https://github.com/gergelyk/python-gridview>\n* Package: <https://pypi.python.org/pypi/gridview>\n* Author: [Grzegorz Krasoń](mailto:grzegorz.krason@gmail.com)\n* License: [MIT](LICENSE)\n\n## Requirements\n\nThis package requires CPython 3.8 or compatible. If you have other version already installed, you can switch using `pyenv`. It must be installed as described in the [manual](https://github.com/pyenv/pyenv).\n\n```sh\npyenv install 3.8.2\npyenv local 3.8.2\n```\n\n## Installation\n\n```sh\npip install gridview\n```\n\n## Development\n\n```sh\n# Preparing environment\npip install --user poetry  # unless already installed\npoetry install\n\n# Auto-formatting\npoetry run docformatter -ri gridview tests\npoetry run isort -rc gridview tests\npoetry run yapf -r -i gridview tests\n\n# Checking coding style\npoetry run flake8 gridview tests\n\n# Checking composition and quality\npoetry run vulture gridview tests\npoetry run mypy gridview tests\npoetry run pylint gridview tests\npoetry run bandit gridview tests\npoetry run radon cc gridview tests\npoetry run radon mi gridview tests\n\n# Testing with coverage\npoetry run pytest --cov gridview --cov tests\n\n# Rendering documentation\npoetry run mkdocs serve\n\n# Building package\npoetry build\n\n# Releasing\npoetry version minor  # increment selected component\ngit commit -am "bump version"\ngit push\ngit tag ${$(poetry version)[2]}\ngit push --tags\npoetry build\npoetry publish\npoetry run mkdocs build\npoetry run mkdocs gh-deploy -b gh-pages\n```\n\n## Donations\n\nIf you find this software useful and you would like to repay author\'s efforts you are welcome to use following button:\n\n[![Donate](https://www.paypalobjects.com/en_US/PL/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=D9KUJD9LTKJY8&source=url)\n\n',
    'author': 'Grzegorz Krasoń',
    'author_email': 'grzegorz.krason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gergelyk.github.io/python-gridview',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
