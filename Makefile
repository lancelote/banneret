help:
	@echo "install"
	@echo "    Install banneret"
	@echo "uninstall"
	@echo "    Uninstall banneret"

install:
	cp -f src/banneret.sh ~/bin/bnrt
	chmod +x ~/bin/bnrt

uninstall:
	rm ~/bin/banneret.sh
