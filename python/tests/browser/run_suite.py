"""Run the existing system suite inside a real browser's Pyodide runtime."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright


PYODIDE_VERSION = "314.0.7"
PYTHON_ROOT = Path(__file__).resolve().parents[2]


def main():
	"""Load StateMint and its test suite into Pyodide and propagate failures."""
	files = {
		"StateMint/" + path.name: path.read_text(encoding="utf-8")
		for path in sorted((PYTHON_ROOT / "StateMint").glob("*.py"))
	}
	files["test_suite.py"] = (
		PYTHON_ROOT / "tests" / "test_suite.py"
	).read_text(encoding="utf-8")
	handler = partial(SimpleHTTPRequestHandler, directory=str(PYTHON_ROOT))
	with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
		thread = Thread(target=server.serve_forever, daemon=True)
		thread.start()
		try:
			with sync_playwright() as playwright:
				browser = playwright.chromium.launch()
				try:
					page = browser.new_page()
					page.on("console", lambda message: print(message.text, flush=True))
					page.goto(f"http://127.0.0.1:{server.server_port}/")
					page.evaluate(
						"""async ({version, files}) => {
							const indexURL = `https://cdn.jsdelivr.net/pyodide/v${version}/full/`;
							const {loadPyodide} = await import(indexURL + "pyodide.mjs");
							const pyodide = await loadPyodide({
								indexURL,
								stdout: line => console.log(line),
								stderr: line => console.error(line),
							});
							await pyodide.loadPackage(["sympy", "numpy"]);
							pyodide.FS.mkdirTree("/home/pyodide/StateMint");
							for (const [name, source] of Object.entries(files)) {
								pyodide.FS.writeFile("/home/pyodide/" + name, source);
							}
							await pyodide.runPythonAsync(`
import unittest
import test_suite

suite = unittest.defaultTestLoader.loadTestsFromModule(test_suite)
if not suite.countTestCases():
    raise RuntimeError("No system tests were discovered")
result = unittest.TextTestRunner(verbosity=2).run(suite)
if not result.wasSuccessful() or result.skipped:
    raise RuntimeError("The Pyodide system suite failed or skipped tests")
`);
						}""",
						{"version": PYODIDE_VERSION, "files": files},
					)
				finally:
					browser.close()
		finally:
			server.shutdown()
			thread.join()


if __name__ == "__main__":
	main()
