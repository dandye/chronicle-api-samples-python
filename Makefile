.PHONY: install dist clean

install:
	python setup.py install

dist:
	python setup.py bdist_wheel

clean:
	rm -rf build/ dist/ *.egg-info/
