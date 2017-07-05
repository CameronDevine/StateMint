var html = 
'<form id="input">' +
'Input Variables:' +
'<br><textarea rows="1" cols="40" id="InVars"></textarea><br>' +
'State Variable Elemental Equations:' +
'<br><textarea rows="3" cols="40" id="StVarElEqns"></textarea><br>' +
'Other Elemental Equations:' +
'<br><textarea rows="3" cols="40" id="OtherElEqns"></textarea><br>' +
'Constraints:' +
'<br><textarea rows="3" cols="40" id="Constraints"></textarea><br>' +
'Output Variables:' +
'<br><textarea rows="1" cols="40" id="OutputVars"></textarea><br>' +
'<button type="button" onclick="StateModel()">Go</button>' +
'</form>' +
'<form id="langform" style="display:none">' +
'<table>' +
'<td><input type="radio" name="langs" id="Equation" onclick="outlang(\'Equation\')">Equation</input></td>' +
'<td><input type="radio" name="langs" id="Latex" onclick="outlang(\'LaTeX\')">LaTeX</input></td>' +
'<td><div id="matlab_div">' +
'<input type="radio" name="langs" id="Matlab" onclick="outlang(\'Matlab\')">MATLAB</input>' +
'</div></td>' +
'<td><input type="radio" name="langs" id="Mathematica" onclick="outlang(\'Mathematica\')">Mathematica</input></td>' +
'<td><input type="radio" name="langs" id="Python" onclick="outlang(\'Python\')">Python</input></td>' +
'</table>' +
'</form>' +
'<form id="form" style="display:none">' +
'<table>' +
'<td><input type="radio" name="eqsform" id="StateSpace" onclick="eqform(\'StateSpace\')">\\(\\dot{x}=Ax+Bu\\)</input></td>' +
'<td><div name="nonstandard_div" style="display:none">' +
'<input type="radio" name="eqsform" id="StateSpaceN" onclick="eqform(\'StateSpaceN\')">\\(\\dot{x}=Ax+Bu+E\\dot{u}\\)</input>' +
'</div></td>' +
'<td><div name="nonstandard_div" style="display:none">' +
'<input type="radio" name="eqsform" id="StateSpaceP" onclick="eqform(\'StateSpaceP\')">\\(\\dot{x}=Ax\'+B\'u\\)</input>' +
'</div></td>' +
'<td><div id="tf_div">' +
'<input type="radio" name="eqsform" id="TF" onclick="eqform(\'TF\')">\\(H(s)\\)</input>' +
'</div></td>' +
'<td><div id="nonlinear_div" style="display:none">' +
'<input type="radio" name="eqsform" id="eq" onclick="eqform(\'eq\')">\\(f(x,u)\\)</input>' +
'</div></td>' +
'</table>' +
'</form>' +
'<div id="output"></div>';

var data = {};
var use_lang = "";
var last_form = "";
var jpeg = null;
var Exif;

function callback() {
	console.log(data);
	document.getElementById("output").innerHTML = "";
	document.getElementById("matlab_div").style["display"] = "block";
	document.getElementById("nonlinear_div").style["display"] = "none";
	if (data.Nonlinear) {
		console.log("nonlinear");
		document.getElementById("matlab_div").style["display"] = "block";
		document.getElementById("nonlinear_div").style["display"] = "block";
	}
	document.getElementsByName("nonstandard_div")[0].style["display"] = "none";
	document.getElementsByName("nonstandard_div")[1].style["display"] = "none";
	if (data.Nonstandard) {
		console.log("nonstandard");
		document.getElementsByName("nonstandard_div")[0].style["display"] = "block";
		document.getElementsByName("nonstandard_div")[1].style["display"] = "block";
	}
	document.getElementById("langform").style["display"] = "block";
	document.getElementById("form").style["display"] = "block";
	console.log(MathJax.Hub.Queue(["Typeset",MathJax.Hub,"form"]));
	document.getElementById("Equation").checked = true;
	outlang("Equation");
	document.getElementById("StateSpace").checked = true;
	eqform("StateSpace");
	}

function eqform(type) {
	last_form = type;
	if (use_lang == "Equation") {
		var codes = data.LaTeX;
		if (type == "StateSpace") {
			output("<p>$$\\dot{x}=" + codes.A + "x+" + codes.B + "u$$</p><p>$$y=" + codes.C + "x+" + codes.D + "u$$</p>");
		} else if (type == "StateSpaceN") {
			output("<p>$$\\dot{x}=" + codes.A + "x+" + codes.B + "u+" + codes.E + "\\dot{u}$$</p><p>$$y=" + codes.C + "x+" + codes.D + "u+" + codes.F + "\\dot{u}$$</p>");
		} else if (type == "StateSpaceP") {
			output("<p>$$\\dot{x}'=" + codes.A + "x'+" + codes.Bp + "u$$</p><p>$$y=" + codes.C + "x'+" + codes.Dp + "u$$</p>");
		} else if (type == "TF") {
			output("<p>$$H(s)=" + codes.TF + "$$</p>");
		} else if (type == "eq") {
			output("<p>$$\\dot{x}=f(x,u)=" + codes.StateEq + "$$</p><p>$$y=h(x,u)=" + codes.OutEq + "$$</p>");
		}
		typeset();
	} else if (use_lang == "Mathematica") {
		var codes = data.Mathematica;
		if (type == "StateSpace") {
			output("<p>{a->" + codes.A + ",b->" + codes.B + ",c->" + codes.C + ",d->" + codes.D + "}</p>");
		} else if (type == "StateSpaceN") {
			output("<p>{a->" + codes.A + ",b->" + codes.B + ",c->" + codes.C + ",d->" + codes.D + ",e->" + codes.E + ",f->" + codes.F + "}</p>");
		} else if (type == "StateSpaceP") {
			output("<p>{a->" + codes.A + ",bp->" + codes.Bp + ",c->" + codes.C + ",dp->" + codes.Dp + "}</p>");
		} else if (type == "eq") {
			output("<p>f(x,u): " + codes.StateEq + "</p><p>h(x,u): " + codes.OutEq + "</p>");
		}
	} else if (use_lang == "LaTeX") {
		var codes = data.LaTeX;
		if (type == "StateSpace") {
			output("<p><table><tr><td>A </td><td>" + codes.A + "</td></tr><tr><td>B </td><td>" + codes.B + "</td></tr><tr><td>C </td><td>" + codes.C + "</td></tr><tr><td>D </td><td>" + codes.D + "</td></tr></table></p>");
		} else if (type == "StateSpaceN") {
			output("<p><table><tr><td>A </td><td>" + codes.A + "</td></tr><tr><td>B </td><td>" + codes.B + "</td></tr><tr><td>C </td><td>" + codes.C + "</td></tr><tr><td>D </td><td>" + codes.D + "</td></tr><tr><td>E </td><td>" + codes.E + "</td></tr><tr><td>F </td><td>" + codes.F + "</td></tr></table></p>");
		} else if (type == "StateSpaceP") {
			output("<p><table><tr><td>A </td><td>" + codes.A + "</td></tr><tr><td>B' </td><td>" + codes.Bp + "</td></tr><tr><td>C </td><td>" + codes.C + "</td></tr><tr><td>D' </td><td>" + codes.Dp + "</td></tr></table></p>");
		} else if (type == "TF") {
			output("<p>" + codes.TF + "</p>");
		} else if (type == "eq") {
			output("<p><table><tr><td>State Equation </td><td>" + codes.StateEq + "</td></tr><tr><td>Output Equation </td><td>" + codes.OutEq + "</td></tr></table></p>");
		}
	} else {
		var codes = data[use_lang];
		if (type == "StateSpace") {
			output("<p>A=" + codes.A + "</p><p>B=" + codes.B + "</p><p>C=" + codes.C + "</p><p>D=" + codes.D + "</p>");
		} else if (type == "StateSpaceN") {
			output("<p>A=" + codes.A + "</p><p>B=" + codes.B + "</p><p>C=" + codes.C + "</p><p>D=" + codes.D + "</p><p>E=" + codes.E + "</p><p>F=" + codes.F + "</p>");
		} else if (type == "StateSpaceP") {
			output("<p>A=" + codes.A + "</p><p>Bp=" + codes.Bp + "</p><p>C=" + codes.C + "</p><p>Dp=" + codes.Dp + "</p>");
		} else if (type == "eq") {
			output("<p>f=" + codes.StateEq + "</p><p>h=" + codes.OutEq + "</p>");
		}
	}
}

function output(html) {
	document.getElementById("output").innerHTML = html;
	}

function typeset() {
	MathJax.Hub.Queue(["Typeset",MathJax.Hub,"output"]);
	}

function outlang(type) {
	use_lang = type;
	set_forms(type);
	eqform(last_form);
	}

function set_forms(type) {
	document.getElementById("tf_div").style["display"] = "none";
	if (type == "Equation" || type == "LaTeX") {document.getElementById("tf_div").style["display"] = "block";}
	if (type != "Equation" && type != "LaTeX" && last_form == "TF") {
		console.log(type != "Equation")
		console.log(type != "LaTeX")
		console.log(last_form == "TF")
		document.getElementById("StateSpace").checked = true;
		eqform("StateSpace");
	}
}

function StateModel() {
	console.log("submit");
	document.getElementById("langform").style["display"] = "none";
	document.getElementById("form").style["display"] = "none";
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
	document.getElementById("output").innerHTML = '<img src="https://d13yacurqjgara.cloudfront.net/users/12755/screenshots/1037374/hex-loader2.gif", alt="Loading">'
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
}

function StateModelHTML() {
	console.log('Adding HTML')
	document.getElementById("StateModelRnDcontainer").innerHTML = html;
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
	a.setAttribute('download', 'StateModelRnD.jpg');
	a.click();
}

function insertImage() {
	var image = new Image();
	image.src = jpeg;
	image.width = 200;
	document.getElementById("imagediv").innerHTML = "";
	var el = $("<div></div>").append(image);
	$("#imagediv").prepend(el);
}

function addImage(event) {
	var file = event.target.files[0];
	if (!file.type.match('image/jpeg.*')) {
		return;
	}
	var reader = new FileReader();
	reader.onload = function(e) {
		jpeg = e.target.result;
		insertImage();
		Exif = piexif.load(jpeg);
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
	if (!file.type.match('image/jpeg.*')) {
		return;
	}
	var reader = new FileReader();
	reader.onload = function(e) {
		jpeg = e.target.result;
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
