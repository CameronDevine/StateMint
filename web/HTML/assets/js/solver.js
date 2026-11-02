// Main-thread client for the StateMint solver worker (assets/js/worker.js).
//
//   StateMintSolver.solve(fields, {tf: bool}) -> Promise of the result body
//   StateMintSolver.onstatus = function(status, detail) {...}
//
// The worker starts loading Pyodide and SymPy as soon as this file runs, so
// it is usually ready by the time the equations are typed. A solve that runs
// longer than TIMEOUT is abandoned and the worker restarted.

var StateMintSolver = (function() {
	var TIMEOUT = 180 * 1000;
	var script = document.currentScript;
	var version = (script && script.getAttribute('data-version')) || '';
	var workerURL = new URL('worker.js', script ? script.src : location.href);
	if (version) {
		workerURL.searchParams.set('v', version);
	}

	var worker = null;
	var nextId = 1;
	var pending = {};
	var api = {status: 'loading', detail: '', onstatus: null, version: version};

	function setStatus(s, detail) {
		api.status = s;
		api.detail = detail || '';
		if (api.onstatus) {
			api.onstatus(s, api.detail);
		}
	}

	function startWorker() {
		setStatus('loading', 'Starting');
		worker = new Worker(workerURL, {type: 'module'});
		worker.onmessage = function(event) {
			var msg = event.data;
			if (msg.type === 'status') {
				setStatus(msg.status, msg.detail);
			} else if (msg.type === 'result' && pending[msg.id]) {
				var p = pending[msg.id];
				delete pending[msg.id];
				clearTimeout(p.timer);
				p.resolve(msg.body);
			}
		};
		worker.onerror = function(event) {
			setStatus('failed', event.message || 'The solver crashed');
		};
	}

	function restart(reason) {
		if (worker) {
			worker.terminate();
		}
		Object.keys(pending).forEach(function(id) {
			clearTimeout(pending[id].timer);
			pending[id].resolve({error: reason});
			delete pending[id];
		});
		startWorker();
	}

	api.solve = function(fields, options) {
		return new Promise(function(resolve) {
			var id = nextId++;
			var timer = setTimeout(function() {
				restart('StateMint took longer than ' + (TIMEOUT / 1000) +
					' seconds and was stopped. The equations may be very large ' +
					'or strongly nonlinear.');
			}, TIMEOUT);
			pending[id] = {resolve: resolve, timer: timer};
			worker.postMessage({id: id, fields: fields, options: options || {}});
		});
	};

	startWorker();
	return api;
})();
