target:
	@echo -e "\033[1mneofetch-win v$(shell grep -oP '(?<=__version__ = ")[^"]*' neofetch_win/__init__.py)\033[0m" \
	"\nUse 'make \033[0;36mtarget\033[0m' where \033[0;36mtarget\033[0m is one of the following:"
	@awk -F ':|##' '/^[^\t].+?:.*?##/ { printf " \033[0;36m%-15s\033[0m %s\n", $$1, $$NF }' $(MAKEFILE_LIST)

# Production tools
install:  ## Install the package
	pip install .

uninstall:  ## Uninstall the package
	pip uninstall neofetch-win -y

reinstall: uninstall install  ## Reinstall the package

# Development tools
venv:  ## Create a virtual environment
	python -m venv .venv

clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./neofetch-win.egg-info

# Maintainer-only commands
upload_pypi:  ## Maintainer only - Upload latest version to PyPi
	@echo Uploading to PyPi...
	pip install .
	python -m build
	twine upload dist/*
	@echo Done!
