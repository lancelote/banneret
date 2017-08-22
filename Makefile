help:
	@echo "deploy"
	@echo "    deploy executable to /usr/local/bin on macOS"

deploy:
	cp bnrt.py bnrt
	chmod +x bnrt
	cp bnrt /usr/local/bin/