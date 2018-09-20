.PHONY: all build upload clean docs

all: build upload clean

build:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

clean:
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	rm -rf docs/html
	rm -rf docs/doctrees

docs:
	sphinx-build -M html docs/ docs/
