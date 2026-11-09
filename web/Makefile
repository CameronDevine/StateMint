# The StateMint web interface is a static site: StateMint itself runs in the
# browser with Pyodide (assets/js/worker.js), so there is no server to deploy.
#
#   make site    build the site into build/ (HTML/ plus the Python package)
#   make serve   build it and serve it at http://localhost:8000
#   make clean   remove build/
#
# Publish by copying build/ to any static host (GitHub Pages, a Django app's
# static files, ...).

.PHONY: site serve clean

PY := ../python/StateMint
VERSION := $(shell sed -n "s/^__version__ = '\(.*\)'/\1/p" $(PY)/__init__.py)+$(shell git rev-parse --short HEAD)

site:
	rm -rf build
	cp -R HTML build
	mkdir -p build/assets/py/StateMint
	cp $(PY)/__init__.py $(PY)/StateMint.py $(PY)/web.py build/assets/py/StateMint/
	sed -i.bak 's/@VERSION@/$(VERSION)/g' build/index.html && rm build/index.html.bak
	@echo "Built build/ (StateMint $(VERSION))"

serve: site
	cd build && python3 -m http.server 8000

clean:
	rm -rf build
