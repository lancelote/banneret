help:
	@echo "install"
	@echo "    Install banneret"
	@echo "uninstall"
	@echo "    Uninstall banneret"

install:
	mv src/banneret.sh ~/bin/

uninstall:
	rm ~/bin/banneret.sh
