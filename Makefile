help:
	@echo "update"
	@echo "    reinstall all required packages"
	@echo "test"
	@echo "    run all the tests"
	@echo "install"
	@echo "    install banneret and dependencies for development"
	@echo "uninstall"
	@echo "    uninstall banneret"

update:
	pipenv update  --dev

test:
	python -m pytest tests

install:
	pipenv install -e .[docker][test] --dev

uninstall:
	pipenv uninstall banneret
