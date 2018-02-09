help:
	@echo "pipenv"
	@echo "    install pipenv for current user"
	@echo "update"
	@echo "    reinstall all required packages"
	@echo "test"
	@echo "    run all the tests"
	@echo "install"
	@echo "    install banneret for development"
	@echo "uninstall"
	@echo "    uninstall banneret"

update:
	pipenv update

test:
	python -m pytest tests

install:
	pipenv install '-e .' --dev

uninstall:
	pipenv uninstall banneret
