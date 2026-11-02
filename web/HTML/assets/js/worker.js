// StateMint solver worker: runs the StateMint Python package in the browser
// with Pyodide, so the web interface needs no server. It is a module worker
// (Pyodide 314 no longer supports classic workers).
//
// Messages in:  {id, fields, options}  where fields maps InVars,
//               StVarElEqns, OtherElEqns, Constraints and OutputVars to
//               their text, and options.tf asks for the transfer function.
// Messages out: {type: 'status', status: 'loading' | 'ready' | 'failed', detail}
//               {type: 'result', id, body}  (body is StateMint.web's dict,
//               or {error: message})

const PYODIDE_VERSION = '314.0.7';
const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v' + PYODIDE_VERSION + '/full/';
const PY_FILES = ['__init__.py', 'StateMint.py', 'web.py'];

// The page passes its version as ?v=… so the Python files are re-fetched
// when StateMint is updated.
const VERSION = new URL(self.location.href).searchParams.get('v') || '';
const PY_BASE = new URL('../py/StateMint/', self.location.href);

function status(s, detail) {
	self.postMessage({type: 'status', status: s, detail: detail || ''});
}

async function start() {
	status('loading', 'Loading Python');
	const {loadPyodide} = await import(PYODIDE_URL + 'pyodide.mjs');
	const pyodide = await loadPyodide({indexURL: PYODIDE_URL});
	status('loading', 'Loading SymPy');
	await pyodide.loadPackage(['sympy']);
	status('loading', 'Loading StateMint');
	pyodide.FS.mkdirTree('/home/pyodide/StateMint');
	await Promise.all(PY_FILES.map(async function(name) {
		var url = new URL(name, PY_BASE);
		if (VERSION) {
			url.searchParams.set('v', VERSION);
		}
		var resp = await fetch(url);
		if (!resp.ok) {
			throw new Error('could not fetch ' + url + ' (' + resp.status + ')');
		}
		pyodide.FS.writeFile('/home/pyodide/StateMint/' + name, await resp.text());
	}));
	var web = pyodide.pyimport('StateMint.web');
	// Warm up: the first solve imports most of SymPy.
	web.solve_json(JSON.stringify({InVars: 'u', StVarElEqns: "x' = q",
		OtherElEqns: 'q = u - x', OutputVars: 'x'}));
	return web;
}

var ready = start().then(function(web) {
	status('ready');
	return web;
}, function(err) {
	status('failed', String(err && err.message || err));
	throw err;
});

self.onmessage = function(event) {
	var msg = event.data;
	ready.then(function(web) {
		var body;
		try {
			var tf = !!(msg.options && msg.options.tf);
			body = JSON.parse(web.solve_json(JSON.stringify(msg.fields), tf));
		} catch (err) {
			body = {error: 'StateMint failed: ' + (err && err.message || err)};
		}
		self.postMessage({type: 'result', id: msg.id, body: body});
	}, function(err) {
		self.postMessage({type: 'result', id: msg.id, body: {
			error: 'The solver could not load (' + (err && err.message || err) +
				'). Check your internet connection and reload the page.'}});
	});
};
