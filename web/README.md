## Web Interface

The web interface lets students and others use StateMint without installing anything.
It is running at [ricopic.one/statemint](https://ricopic.one/statemint/).

### How it works

The page is static. A module Web Worker ([assets/js/worker.js](HTML/assets/js/worker.js)) loads [Pyodide](https://pyodide.org) and SymPy from jsdelivr, writes the StateMint Python package into Pyodide's file system and calls `StateMint.web.solve_json`, which returns the model as LaTeX, MATLAB, Mathematica and Python.
Nothing is sent to a server.
The first visit downloads about 11 MB (cached afterwards); the solver is ready a few seconds after the page loads.

Systems can be saved in the browser (localStorage), downloaded as `.rnd` files (a JPEG of the system's picture whose EXIF UserComment holds the five fields as JSON), or shared as links (`?` followed by the URL-encoded JSON).

### Building

```
make site
```

builds the site into `build/`: the contents of `HTML/` plus the package's `__init__.py`, `StateMint.py` and `web.py` under `assets/py/StateMint/`, cache-busted with the package version.
`make serve` builds it and serves it at http://localhost:8000.
To publish, copy `build/` to any static host; ricopic.one serves it from a Django app (`statemint/` in the homepage repository).

Until version 3 the computation ran in an AWS Lambda function behind API Gateway; that code is in the history (`web/aws`, version 2.1.1).
