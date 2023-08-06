# GridView

Visualize your 2D iterable. See our usage [examples](https://gergelyk.github.io/python-gridview) now!

* Documentation: <https://gergelyk.github.io/python-gridview>
* Repository: <https://github.com/gergelyk/python-gridview>
* Package: <https://pypi.python.org/pypi/gridview>
* Author: [Grzegorz Krasoń](mailto:grzegorz.krason@gmail.com)
* License: [MIT](LICENSE)

## Requirements

This package requires CPython 3.8 or compatible. If you have other version already installed, you can switch using `pyenv`. It must be installed as described in the [manual](https://github.com/pyenv/pyenv).

```sh
pyenv install 3.8.2
pyenv local 3.8.2
```

## Installation

```sh
pip install gridview
```

## Development

```sh
# Preparing environment
pip install --user poetry  # unless already installed
poetry install

# Auto-formatting
poetry run docformatter -ri gridview tests
poetry run isort -rc gridview tests
poetry run yapf -r -i gridview tests

# Checking coding style
poetry run flake8 gridview tests

# Checking composition and quality
poetry run vulture gridview tests
poetry run mypy gridview tests
poetry run pylint gridview tests
poetry run bandit gridview tests
poetry run radon cc gridview tests
poetry run radon mi gridview tests

# Testing with coverage
poetry run pytest --cov gridview --cov tests

# Rendering documentation
poetry run mkdocs serve

# Building package
poetry build

# Releasing
poetry version minor  # increment selected component
git commit -am "bump version"
git push
git tag ${$(poetry version)[2]}
git push --tags
poetry build
poetry publish
poetry run mkdocs build
poetry run mkdocs gh-deploy -b gh-pages
```

## Donations

If you find this software useful and you would like to repay author's efforts you are welcome to use following button:

[![Donate](https://www.paypalobjects.com/en_US/PL/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=D9KUJD9LTKJY8&source=url)

