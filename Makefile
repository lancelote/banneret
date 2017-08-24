help:
	@echo "test"
	@echo "    run all the tests"
	@echo "deploy"
	@echo "    deploy executable to /usr/local/bin on macOS"

test:
	python -m pytest tests

deploy: test
	cp banneret.py bnrt
	chmod +x bnrt
	cp bnrt /usr/local/bin/
	rm bnrt