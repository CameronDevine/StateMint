var data = {};
var use_lang = "";
var last_form = "";
var jpeg = null;
var Exif;
var default_form = 'StateSpace';
var tutorial_loaded = false;

function callback() {
	console.log(data);
	$('#matlabButton').show();
	$('#eq').hide();
	$('#TF').show();
	default_form = 'StateSpace';
	if (data.Nonlinear) {
		console.log("nonlinear");
		$('#matlabButton').hide();
		$('#eq').show();
		$('#TF').hide();
		default_form = 'StateSpace';
	}
	$('#StateSpaceN').hide();
	$('#StateSpaceP').hide();
	$('#StateSpace').show();
	if (data.Nonstandard) {
		console.log("nonstandard");
		$('#StateSpaceN').show();
		$('#StateSpaceP').show();
		$('#StateSpace').hide();
		default_form = 'StateSpaceN';
	}
	if (data.Parameters && data.Parameters.length) {
		$('#params').html('Parameters: ' + data.Parameters.map(function(p) {
			return '$' + p + '$';
		}).join(', ') + '. <span class="text-muted">(If one of these is ' +
			'meant to be a variable, its equation is missing.)</span>').show();
	} else {
		$('#params').hide();
	}
	outlang("Equation");
	eqform(default_form);
	$('#page6button').show();
	$('#page6li').show();
	$('#page6').show();
	$('#inputButtons').hide();
	setTimeout(function() {
		$('#page4button').click();
		setTimeout(function () {
			$('#LoadingPage').hide();
			$('#page4button').click();
		}, 500);
	}, 200);
}

function output(names, equations) {
	$('#output .buttons').hide().slice(0, names.length).show();
	for (i = 0; i < names.length; i++) {
		$('#output h4').eq(i).html(names[i]);
		$('#output strong').eq(i).html(equations[i]);
		$('#output textarea').eq(i).val(equations[i]);
	}
	$('#output').show();
}

function eqform(type) {
	last_form = type;
	$('#eqButtons :button').removeClass('btn-primary');
	$('#eqButtons :button').addClass('btn-default');
	$('#' + type).removeClass('btn-default');
	$('#' + type).addClass('btn-primary');
	if (use_lang == "Equation") {
		var codes = data.LaTeX;
		if (type == "StateSpace") {
			output(["State", "Output"], [
				"$$\\dot{x}=" + codes.A + "x+" + codes.B + "u$$",
				"$$y=" + codes.C + "x+" + codes.D + "u$$"]);
		} else if (type == "StateSpaceN") {
			output(["State", "Output"], [
				"$$\\dot{x}=" + codes.A + "x+" + codes.B + "u+" + codes.E + "\\dot{u}$$",
				"$$y=" + codes.C + "x+" + codes.D + "u+" + codes.F + "\\dot{u}$$"]);
		} else if (type == "StateSpaceP") {
			output(["State", "Output"], [
				"$$\\dot{x}'=" + codes.A + "x'+" + codes.Bp + "u$$",
				"$$y=" + codes.C + "x'+" + codes.Dp + "u" +
					(data.NonzeroF ? "+" + codes.F + "\\dot{u}" : "") + "$$"]);
		} else if (type == "TF") {
			output(["Transfer Function"], [
				"$$H(s)=" + codes.TF + "$$"]);
		} else if (type == "eq") {
			output(["State", "Output"], [
				"$$\\dot{x}=f(x,u)=" + codes.StateEq + "$$",
				"$$y=h(x,u)=" + codes.OutEq + "$$"]);
		} else if (type == "vector") {
			output(["State Vector", "Input Vector", "Output Vector"], [
				"$$x=" + codes.StateVec + "$$",
				"$$u=" + codes.InputVec + "$$",
				"$$y=" + codes.OutputVec + "$$"]);
		}
		typeset();
		$('#params').show();
	} else if (use_lang == "Mathematica") {
		var codes = data.Mathematica;
		if (type == "StateSpace") {
			output(['State Equation Matrices'], [
				"{a->" + codes.A + ",b->" + codes.B + ",c->" + codes.C + ",d->" + codes.D + "}"]);
		} else if (type == "StateSpaceN") {
			output(['State Equation Matrices'], [
				"{a->" + codes.A + ",b->" + codes.B + ",c->" + codes.C + ",d->" + codes.D + ",e->" + codes.E + ",f->" + codes.F + "}"]);
		} else if (type == "StateSpaceP") {
			output(['State Equation Matrices'], [
				"{a->" + codes.A + ",bp->" + codes.Bp + ",c->" + codes.C + ",dp->" + codes.Dp + "}"]);
		} else if (type == "eq") {
			output(['State Equation', 'Output Equation'],
				[codes.StateEq, codes.OutEq]);
		}
	} else if (use_lang == "LaTeX") {
		var codes = data.LaTeX;
		if (type == "StateSpace") {
			output(['A', 'B', 'C', 'D'],
				[codes.A, codes.B, codes.C, codes.D]);
		} else if (type == "StateSpaceN") {
			output(['A', 'B', 'C', 'D', 'E', 'F'],
				[codes.A, codes.B, codes.C, codes.D, codes.E, codes.F]);
		} else if (type == "StateSpaceP") {
			output(['A', 'B\'', 'C', 'D\''],
				[codes.A, codes.Bp, codes.C, codes.Dp]);
		} else if (type == "TF") {
			output(['Transfer Function'], [codes.TF]);
		} else if (type == "eq") {
			output(['State Equation', 'Output Equation'],
				[codes.StateEq, codes.OutEq]);
		} else if (type == "vector") {
			output(["State Vector", "Input Vector", "Output Vector"],
				[codes.StateVec, codes.InputVec, codes.OutputVec]);
		}
	} else {
		var codes = data[use_lang];
		if (type == "StateSpace") {
			output(['A', 'B', 'C', 'D'],
				[codes.A, codes.B, codes.C, codes.D]);
		} else if (type == "StateSpaceN") {
			output(['A', 'B', 'C', 'D', 'E', 'F'],
				[codes.A, codes.B, codes.C, codes.D, codes.E, codes.F]);
		} else if (type == "StateSpaceP") {
			output(['A', 'B\'', 'C', 'D\''],
				[codes.A, codes.Bp, codes.C, codes.Dp]);
		} else if (type == "eq") {
			output(['State Equation', 'Output Equation'],
				[codes.StateEq, codes.OutEq]);
		}
	}
}

function typeset() {
	MathJax.Hub.Queue(["Typeset", MathJax.Hub, "output"]);
	MathJax.Hub.Queue(["Typeset", MathJax.Hub, "params"]);
	}

function outlang(type) {
	$('#langButtons :button').removeClass('btn-primary');
	$('#langButtons :button').addClass('btn-default');
	$('#' + type.toLowerCase() + 'Button').removeClass('btn-default');
	$('#' + type.toLowerCase() + 'Button').addClass('btn-primary');
	use_lang = type;
	set_forms(type);
	eqform(last_form);
	}

function set_forms(type) {
	$('#TF').hide();
	$('#vector').hide();
	if (type == "Equation" || type == "LaTeX") {
		if (!data.Nonlinear) {
			$('#TF').show();
		}
		$('#vector').show();
	}
	if (type != "Equation" && type != "LaTeX" && (last_form == "TF" || last_form == "vector")) {
		eqform(default_form);
	}
}

function escapeHTML(text) {
	return $('<div>').text(text).html();
}

function showError(text) {
	$('#error').html(escapeHTML(text).replace(/\n/g, '<br>'));
	$('#errorRef').modal();
	$('#LoadingPage').hide();
	$('#page3button').click();
}

function StateModel() {
	$('#page6').hide();
	$('#inputButtons').show();
	$('#page6button').hide();
	$('#LoadingPage').show();
	$('#LoadingPageLink').click();
	StateMintSolver.solve(getData()).then(function(result) {
		if (result.error) {
			showError(result.error);
			return;
		}
		data = result;
		callback();
	});
}

function loadExample(num, scroll) {
	if (num == 1) {
		document.getElementById("InVars").value = "vS";
		document.getElementById("StVarElEqns").value = "vMB' = 1/MB * fMB,\nvMW' = 1/MW * fMW,\nfKS' = KS * vKS,\nfKT' = KT * vKT";
		document.getElementById("OtherElEqns").value = "fBS = BS * vBS,\nfBT = BT * vBT";
		document.getElementById("Constraints").value = "fMB = fKS + fBS,\nfMW = fKT + fBT - fKS - fBS,\nvKS = vMW - vMB,\nvKT = vS - vMW,\nvBS = vMW - vMB,\nvBT = vS - vMW";
		document.getElementById("OutputVars").value = "vMB, vMW, fKS, fKT, fBS, fBT";
		$('#exampleDesc').html('A model of the suspension system of one wheel of a car including tire elasticity, damping, and mass, suspension springs and shocks, and body mass.');
	} else if (num == 2) {
		document.getElementById("InVars").value = "Fs";
		document.getElementById("StVarElEqns").value = "vm' = Fm/m,\nFK1' = K1 * vK1";
		document.getElementById("OtherElEqns").value = "FB2 = B2 * vB2,\nvB1 = FB1/B1,\nvK2 = FK2' / K2";
		document.getElementById("Constraints").value = "vK1 = vK2 - vB1,\nvB2 = vm,\nFK2 = Fs - FK1,\nFB1 = FK1,\nFm = Fs - FB2";
		document.getElementById("OutputVars").value = "vB1";
		$('#exampleDesc').html('A model of a damped mass driven by a force source through a parallel linkage of a spring and a series combination of a damper and a spring.');
	} else if (num == 3) {
		document.getElementById("InVars").value = "Fp, Fr";
		document.getElementById("StVarElEqns").value = "vm' = Fm / m";
		document.getElementById("OtherElEqns").value = "Fd = cd * vd**2";
		document.getElementById("Constraints").value = "Fm = Fp - Fr - Fd,\nvd = vm";
		document.getElementById("OutputVars").value = "vm";
		$('#exampleDesc').html('A model of an idealized car driving down a straight road including propulsive force, nonlinear aerodynamic drag, constant rolling resistance, and car mass.');
	}
	$('#exampleImage').prop('src', 'examples/example' + num + '.svg');
	insertImage('examples/example' + num + '.svg')
	fetch('examples/example' + num + '.jpg').then(function(resp) {
		resp.blob().then(function(blob) {
			reader = new FileReader();
			reader.onloadend = function() {
				jpeg = reader.result;
				Exif = piexif.load(jpeg);
			}
			reader.readAsDataURL(blob);
		});
	});
	if (scroll) {
		$('#page3button').click();
	}
}

function getData() {
	return {
	  	"InVars": document.getElementById("InVars").value,
		"StVarElEqns": document.getElementById("StVarElEqns").value,
		"OtherElEqns": document.getElementById("OtherElEqns").value,
		"Constraints": document.getElementById("Constraints").value,
		"OutputVars": document.getElementById("OutputVars").value
	};
}

function download() {
	if (jpeg == null) {
		addBlank(download);
		return;
	}
	var saveData = getData();
	Exif.Exif['37510'] = JSON.stringify(saveData);
	var exifBytes = piexif.dump(Exif);
	var rnd = piexif.insert(exifBytes, jpeg);
	var str = atob(rnd.split(",")[1]);
	var data = [];
	for (var p = 0; p < str.length; p++) {
		data[p] = str.charCodeAt(p);
	}
	var ua = new Uint8Array(data);
	var blob = new Blob([ua], {type: "image/jpeg"});
	var url = window.URL.createObjectURL(blob);
	var a = document.createElement('a');
	a.setAttribute('href', url);
	a.setAttribute('download', 'system.rnd');
	a.click();
}

function insertImage(image) {
	$('#systemImage').prop('src', image);
}

function convert() {
	var canvas = document.createElement("canvas");
	var image = new Image();
	image.onload = function() {
		canvas.width = image.width;
		canvas.height = image.height;
		var context = canvas.getContext("2d");
		context.drawImage(image, 0, 0);
		jpeg = canvas.toDataURL("image/jpeg");
		Exif = piexif.load(jpeg);
	}
	image.src = jpeg;
}

function addImage(event) {
	var file = event.target.files[0];
	var reader = new FileReader();
	reader.onload = function(e) {
		jpeg = e.target.result;
		var type = jpeg.split(",").slice(0)[0]
		insertImage(jpeg);
		if (type != "data:image/jpeg;base64" && type != "data:image/jpg;base64") {
			convert();
		} else {
			Exif = piexif.load(jpeg);
		}
		$('#page3button').click();
	}
	reader.readAsDataURL(file);
}

function addBlank(callback) {
	console.log('import blank white image and read its exif');
	var canvas = document.createElement("canvas");
	var context = canvas.getContext('2d');
	convimg = new Image();
	convimg.src = 'assets/img/blank.jpg';
	convimg.onload = function () {
		context.drawImage(convimg, 100, 100);
		jpeg = canvas.toDataURL("image/jpeg");
		Exif = piexif.load(jpeg);
		Exif.Exif['37500'] = 'blank';
		callback();
	}
}

function addEquations(data) {
		document.getElementById("InVars").value = data.InVars;
		document.getElementById("StVarElEqns").value = data.StVarElEqns;
		document.getElementById("OtherElEqns").value = data.OtherElEqns;
		document.getElementById("Constraints").value = data.Constraints;
		document.getElementById("OutputVars").value = data.OutputVars;
}

function loadRnd(dataURL) {
	// A .rnd file is a JPEG, but browsers and servers label it variously
	// (no type, application/octet-stream, application/prs.nprend), and
	// piexif only reads image/jpeg data URLs.
	jpeg = "data:image/jpeg;base64," + dataURL.slice(dataURL.indexOf(',') + 1);
	Exif = piexif.load(jpeg);
	if (Exif.Exif['37500'] != 'blank') {
		insertImage(jpeg);
	}
	addEquations(JSON.parse(Exif.Exif['37510']));
	StateModel();
}

function readBlob(blob) {
	var reader = new FileReader();
	reader.onload = function(e) {
		try {
			loadRnd(e.target.result);
		} catch (err) {
			showError('This file is not a StateMint .rnd file (' + err + ').');
		}
	}
	reader.readAsDataURL(blob);
}

function importData(event) {
	var file = event.target.files[0];
	if (file.name.split(".").slice(-1)[0] != "rnd" && !file.type.match('image/jpeg.*')) {
		showError('Choose a StateMint .rnd file.');
		return;
	}
	readBlob(file);
}

// ?open=name opens systems/name.rnd, a system published with the site (the
// System Dynamics notes link these).
function openSystem(name) {
	fetch('systems/' + name + '.rnd').then(function(resp) {
		if (!resp.ok) {
			throw new Error('there is no system named "' + name + '"');
		}
		return resp.blob();
	}).then(readBlob, function(err) {
		showError('Could not open the system: ' + err.message);
	});
}

function copyEq(num) {
	var text = $('#output textarea').eq(num).val();
	if (navigator.clipboard && navigator.clipboard.writeText) {
		navigator.clipboard.writeText(text).then(function() {
			notify('Copied');
		});
	} else {
		$('#output textarea').eq(num).show().select();
		document.execCommand('Copy');
		$('#output textarea').eq(num).hide();
	}
}

function restart() {
	$('#page1button').click();
	scrolPos = $(document).scrollTop();
	while ($(document).scrollTop() != scrolPos) {
		scrolPos = $(document).scrollTop();
	}
	window.location.reload();
}

var SAVE_PREFIX = 'stmt_';

function storage() {
	try {
		return window.localStorage;
	} catch (err) {
		return null;
	}
}

function migrateCookies() {
	var store = storage();
	if (!store || typeof Cookies === 'undefined') {
		return;
	}
	var cookies = Cookies.get();
	Object.keys(cookies).forEach(function(name) {
		if (name.slice(0, SAVE_PREFIX.length) == SAVE_PREFIX) {
			try {
				if (store.getItem(name) === null) {
					store.setItem(name, cookies[name]);
				}
				Cookies.remove(name);
			} catch (err) {}
		}
	});
}

function savedNames() {
	var store = storage();
	var names = [];
	if (!store) {
		return names;
	}
	for (var i = 0; i < store.length; i++) {
		var key = store.key(i);
		if (key.slice(0, SAVE_PREFIX.length) == SAVE_PREFIX) {
			names.push(key.slice(SAVE_PREFIX.length));
		}
	}
	return names.sort();
}

function list_saved() {
	var template = '<tr><td style="vertical-align:middle"><h4><strong></strong></h4></td><td style="vertical-align:middle;width:40px"><i class="material-icons" style="font-size:36px">folder_open</i></td><td style="vertical-align:middle;width:40px"><i class="material-icons" style="font-size:36px">delete_outline</i></td></tr>';
	var names = savedNames();
	var body = $('#saved tbody').empty();
	names.forEach(function(name) {
		var row = $(template);
		row.find('strong').text(name);
		body.append(row);
	});
	if (names.length > 0) {
		$('#saved').closest('.col-sm-6').show();
		$('#fileUploadLink').parent().addClass('col-sm-6');
	} else {
		$('#saved').closest('.col-sm-6').hide()
		$('#fileUploadLink').parent().removeClass('col-sm-6');
	}
}

function save() {
	var store = storage();
	var name = $('#saveName').val().trim();
	if (!store || !name) {
		return;
	}
	try {
		store.setItem(SAVE_PREFIX + name, JSON.stringify(getData()));
	} catch (err) {
		showError('Could not save: ' + err);
	}
	list_saved();
}

function openClick(data) {
	var store = storage();
	if (!store) {
		return;
	}
	if (!data.open) {
		store.removeItem(SAVE_PREFIX + data.name);
		list_saved()
	} else {
		var system = JSON.parse(store.getItem(SAVE_PREFIX + data.name));
		addEquations(system);
		$('#saveName').val(data.name);
		StateModel();
	}
}

function notify(message) {
	$.notify({
		message: message
	},{
		allow_dismiss: false,
		placement: {
			from: 'top',
			align: 'left'},
		delay: 1500,
		onShow: function() {
			this.css({
				'width':'auto',
				'height':'auto',
				'background': '#e6e7ea',
				'color': 'inherit',
				'border-color': '#e6e7ea',
				'box-shadow': '0 0 10px #b5b5b5'});
		}
	});
}

function share() {
	var url = location.origin + location.pathname + '?' +
		encodeURIComponent(JSON.stringify(getData()));
	if (navigator.clipboard && navigator.clipboard.writeText) {
		navigator.clipboard.writeText(url).then(function() {
			notify('Link copied to clipboard');
		}, function() {
			window.prompt('Copy this link:', url);
		});
	} else {
		window.prompt('Copy this link:', url);
	}
}

function loadFromURL() {
	var open = /^\?open=([A-Za-z0-9_-]+)$/.exec(window.location.search);
	if (open) {
		openSystem(open[1]);
	} else if (window.location.search.length > 1) {
		try {
			addEquations(JSON.parse(decodeURIComponent(window.location.search.slice(1))));
		} catch (err) {
			return;
		}
		StateModel();
		$(window).load(function() {
			$('#LoadingPageLink').click();
		});
	}
}

function tutorial() {
	MathJax.Hub.Queue(["Typeset", MathJax.Hub, 'tutorialRef']);
}

function loadTutorial() {
	fetch('tutorial/tutorial.md').then(function(resp) {
		resp.text().then(function(data) {
			body = $('#tutorialRef').find('.modal-body')
			body.html(window.markdownit().render(
				data.split('\\\\').join('\\\\\\\\')));
			body.find('a').each(function() {
				$(this).attr('target', '_blank');
			});
		});
	});
}

$(document).ready(function() {
	migrateCookies();
	list_saved();
	StateMintSolver.onstatus = solverStatus;
	solverStatus(StateMintSolver.status, StateMintSolver.detail);
	loadFromURL();
	$('#saved').click(function(event) {
		openClick({
			name: $(event.target).closest('tr').find('strong').html(),
			open: $(event.target).closest('td').index() != 2});
	});
	$('[data-toggle="tooltip"]').tooltip({delay: {hide: 1500}});
	MathJax.Hub.Config({
		tex2jax: {
			inlineMath: [['$', '$']]
		}
	});
	loadTutorial();
});

function solverStatus(status, detail) {
	var el = $('#solverStatus');
	if (status == 'ready') {
		el.text('Solver ready').fadeOut(2000);
	} else if (status == 'failed') {
		el.stop(true).show().text('The solver could not load: ' + detail);
	} else {
		el.stop(true).show().text('Loading the solver' + (detail ? ': ' + detail : '') + '…');
	}
}
