upload:
	@echo Uploading to PyPi...
	python setup.py install
	python setup.py sdist
	twine upload dist/*
	@echo Done!

clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./neofetch_win.egg-info

reinstall: uninstall install

install:
	pip install .

uninstall:
	pip uninstall neofetch-win -y
