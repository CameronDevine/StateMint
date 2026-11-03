.PHONY: test build check upload clean docs

test:
	python -m pytest

docs:
	sphinx-build -W docs/ docs/build

build: clean
	python -m build

check: build
	python -m twine check --strict dist/*

upload: check
	python -m twine upload dist/*

clean:
	rm -rf *.egg-info dist build docs/build
