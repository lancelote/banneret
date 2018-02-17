help:
	@echo "install"
	@echo "    Install banneret and dependencies for development"
	@echo "lint"
	@echo "    Run linters"
	@echo "test"
	@echo "    Run all the tests"
	@echo "uninstall"
	@echo "    Uninstall banneret"
	@echo "update"
	@echo "    Reinstall all required packages"

install:
	pipenv install -e .[docker,test,lint] --dev

lint:
	python -m pylint --rcfile pylintrc/code.ini banneret
	python -m pylint --rcfile pylintrc/test.ini tests
	python -m pydocstyle banneret
	python -m pycodestyle --select E,W .
	python -m mypy . --ignore-missing-imports

test:
	python -m pytest tests

uninstall:
	pipenv uninstall banneret

update:
	pipenv update  --dev
