help:
	@echo "deploy"
	@echo "    deploy executable to /usr/local/bin on macOS"
	@echo "deps"
	@echo "    install all dependencies (don't forget to activate venv!)"
	@echo "test"
	@echo "    run all the tests"

deps:
	pip install -r requirements.txt

test:
	python -m pytest tests

deploy: test
	cp banneret.py bnrt
	chmod +x bnrt
	cp bnrt /usr/local/bin/
	rm bnrt