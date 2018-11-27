.PHONY: build upload clean docs

docs:
	sphinx-build docs/ docs/build

build:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

clean:
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	rm -rf docs/build
