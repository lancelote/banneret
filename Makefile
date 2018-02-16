help:
	@echo "update"
	@echo "    Reinstall all required packages"
	@echo "test"
	@echo "    Run all the tests"
	@echo "install"
	@echo "    Install banneret and dependencies for development"
	@echo "uninstall"
	@echo "    Uninstall banneret"

update:
	pipenv update  --dev

test:
	python -m pytest tests

install:
	pipenv install -e .[docker,test] --dev

uninstall:
	pipenv uninstall banneret
