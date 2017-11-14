var data = {};
var use_lang = "";
var last_form = "";
var jpeg = null;
var Exif;

function callback() {
	console.log(data);
//	document.getElementById("output").innerHTML = "";
	$('#matlabButton').show();
	$('#eq').hide();
	if (data.Nonlinear) {
		console.log("nonlinear");
		$('#matlabButton').hide();
		$('#eq').show();
	}
	$('#StateSpaceN').hide();
	$('#StateSpaceP').hide();
	if (data.Nonstandard) {
		console.log("nonstandard");
		$('#StateSpaceN').show();
		$('#StateSpaceP').show();
	}
	outlang("Equation");
	eqform("StateSpace");
	$('#page4button').click();
	setTimeout(function () {
		$('#LoadingPage').hide();
		$('#page4button').click();
		}, 500)
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
				"$$y=" + codes.C + "x'+" + codes.Dp + "u$$"]);
		} else if (type == "TF") {
			output(["Transfer Function"], [
				"$$H(s)=" + codes.TF + "$$"]);
		} else if (type == "eq") {
			output(["State", "Output"], [
				"$$\\dot{x}=f(x,u)=" + codes.StateEq + "$$",
				"$$y=h(x,u)=" + codes.OutEq + "$$"]);
		}
		typeset();
	} else if (use_lang == "Mathematica") {
		var codes = data.Mathematica;
		if (type == "StateSpace") {
			output(['State Equation Matricies'], [
				"{a->" + codes.A + ",b->" + codes.B + ",c->" + codes.C + ",d->" + codes.D + "}"]);
		} else if (type == "StateSpaceN") {
			output(['State Equation Matricies'], [
				"{a->" + codes.A + ",b->" + codes.B + ",c->" + codes.C + ",d->" + codes.D + ",e->" + codes.E + ",f->" + codes.F + "}"]);
		} else if (type == "StateSpaceP") {
			output(['State Equation Matricies'], [
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
	MathJax.Hub.Queue(["Typeset",MathJax.Hub,"output"]);
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
	if (type == "Equation" || type == "LaTeX") {$('#TF').show();}
	if (type != "Equation" && type != "LaTeX" && last_form == "TF") {
		console.log(type != "Equation")
		console.log(type != "LaTeX")
		console.log(last_form == "TF")
		eqform("StateSpace");
	}
}

function StateModel() {
	console.log("submit");
	var Client = apigClientFactory.newClient();
	var params = {};
	var body = {};
	var aditionalParams = {
			"queryParams": {
	  				"InVars": document.getElementById("InVars").value,
					"StVarElEqns": document.getElementById("StVarElEqns").value,
					"OtherElEqns": document.getElementById("OtherElEqns").value,
					"Constraints": document.getElementById("Constraints").value,
					"OutputVars": document.getElementById("OutputVars").value
		}
	};
	console.log(aditionalParams)
	$('#LoadingPage').show();
	$('#LoadingPageLink').click();
	Client.stateModelRnDPost(params, body, aditionalParams).then(function(result) {
		console.log(result);
		data = result.data;
		callback();
		}, function(err) {
		console.log(err);
		document.getElementById("output").innerHTML = "<h1>We're sorry. The function has encountered an error</h1>";
	});
}

function loadExample(num) {
	if (num == 1) {
		document.getElementById("InVars").value = "vS";
		document.getElementById("StVarElEqns").value = "vMB' = 1/MB * fMB, vMW' = 1/MW * fMW, fKS' = KS * vKS, fKT' = KT * vKT";
		document.getElementById("OtherElEqns").value = "fBS = BS * vBS, fBT = BT * vBT";
		document.getElementById("Constraints").value = "fMB = fKS + fBS, fMW = fKT + fBT - fKS - fBS, vKS = vMW - vMB, vKT = vS - vMW, vBS = vMW - vMB, vBT = vS - vMW";
		document.getElementById("OutputVars").value = "vMB, vMW, fKS, fKT, fBS, fBT";
	} else if (num == 2) {
		document.getElementById("InVars").value = "Fs";
		document.getElementById("StVarElEqns").value = "vm' = Fm/m, FK1' = K1 * vK1";
		document.getElementById("OtherElEqns").value = "FB2 = B2 * vB2, vB1 = FB1/B1, vK2 = FK2' / K2";
		document.getElementById("Constraints").value = "vK1 = vK2 - vB1, vB2 = vm, FK2 = Fs - FK1, FB1 = FK1, Fm = Fs - FB2";
		document.getElementById("OutputVars").value = "vB1";
	} else if (num == 3) {
		document.getElementById("InVars").value = "Fp, F0";
		document.getElementById("StVarElEqns").value = "vm' = Fm / m";
		document.getElementById("OtherElEqns").value = "Fd = cd * vd**2";
		document.getElementById("Constraints").value = "Fm = Fp - F0 - Fd, vd = vm";
		document.getElementById("OutputVars").value = "vm";
	}
	var canvas = document.createElement("canvas");
	var context = canvas.getContext("2d");
	var image = new Image();
	image.onload = function() {
		canvas.width = image.width;
		canvas.height = image.height;
		context.drawImage(image, 0, 0);
		jpeg = canvas.toDataURL("image/jpeg");
		$('#exampleImage').prop('src', jpeg);
		insertImage();
		Exif = piexif.load(jpeg);
	}
	image.src = "Example" + num + ".jpg";
}

function download() {
	if (jpeg == null) {
		addBlank();
		return;
	}
	var saveData = {
	  	"InVars": document.getElementById("InVars").value,
		"StVarElEqns": document.getElementById("StVarElEqns").value,
		"OtherElEqns": document.getElementById("OtherElEqns").value,
		"Constraints": document.getElementById("Constraints").value,
		"OutputVars": document.getElementById("OutputVars").value
	};
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
	a.setAttribute('download', 'StateModelRnD.rnd');
	a.click();
}

function insertImage() {
	//$('#systemImage').show();
	$('#systemImage').prop('src', jpeg);
//	var image = new Image();
//	image.src = jpeg;
//	image.width = 500;
//	document.getElementById("imagediv").innerHTML = "";
//	var el = $("<div></div>").append(image);
//	$("#imagediv").prepend(el);
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
		insertImage();
		if (type != "data:image/jpeg;base64" && type != "data:image/jpg;base64") {
			convert();
		} else {
			Exif = piexif.load(jpeg);
		}
	}
	reader.readAsDataURL(file);
}

function addBlank() {
	console.log('import blank white image and read its exif');
	var canvas = document.createElement("canvas");
	var context = canvas.getContext('2d');
	convimg = new Image();
	convimg.src = 'blank.jpg';
	convimg.onload = function () {
		context.drawImage(convimg, 100, 100);
		jpeg = canvas.toDataURL("image/jpeg");
		Exif = piexif.load(jpeg);
		Exif.Exif['37500'] = 'blank';
		download();
	}
}

function importData(event) {
	var file = event.target.files[0];
	if (file.name.split(".").slice(-1)[0] != "rnd" && !file.type.match('image/jpeg.*')) {
		console.log("incorrect image type");
		return;
	}
	var reader = new FileReader();
	reader.onload = function(e) {
		jpeg = e.target.result;
		if (jpeg.slice(0, 13) == "data:;base64,") {
			jpeg = "data:image/jpeg;base64," + jpeg.substring(13);
		}
		Exif = piexif.load(jpeg);
		console.log(Exif);
		if (Exif.Exif['37500'] != 'blank') {
			insertImage();
		}
		var loadData = JSON.parse(Exif.Exif['37510']);
		document.getElementById("InVars").value = loadData.InVars;
		document.getElementById("StVarElEqns").value = loadData.StVarElEqns;
		document.getElementById("OtherElEqns").value = loadData.OtherElEqns;
		document.getElementById("Constraints").value = loadData.Constraints;
		document.getElementById("OutputVars").value = loadData.OutputVars;
		StateModel();
	}
	reader.readAsDataURL(file);
}

function copyEq(num) {
	$('#output textarea').eq(num).show();
	$('#output textarea').eq(num).select();
	document.execCommand('Copy');
	$('#output textarea').eq(num).hide()
}
