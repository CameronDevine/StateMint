.PHONEY: all build upload clean

all: build upload clean

build:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

clean:
	rm -r *.egg-info
	rm -r dist
	rm -r build
