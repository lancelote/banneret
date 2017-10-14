help:
	@echo "install"
	@echo "    make and copy executable to /usr/local/bin on macOS"
	@echo "deps"
	@echo "    install all dependencies (don't forget to activate venv!)"
	@echo "test"
	@echo "    run all the tests"
	@echo "uninstall"
	@echo "    removes banneret executable from /usr/local/bin on macOS"

deps:
	pip install -r requirements.txt

test:
	python -m pytest tests

install:
	cp banneret.py bnrt
	chmod +x bnrt
	cp bnrt /usr/local/bin/
	rm bnrt

uninstall:
	rm /usr/local/bin/bnrt
