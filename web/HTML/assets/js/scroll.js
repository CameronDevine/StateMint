var page2id = 'page2';

function pagination() {
	var scrolPos = $(document).scrollTop();
	if ($('#page6').position().top <= scrolPos && $('#page6').is(':visible')) {
		$('li').removeClass('activeDot');
		$('li').eq(3).addClass('activeDot');
		$('#imageContainer').hide();
	} else if ($('#page5').position().top <= scrolPos) {
		$('li').removeClass('activeDot');
		$('li').eq(2).addClass('activeDot');
		if ($('#LoadingPage').is(":visible")) {
			nextPage = $('#LoadingPage').position().top;
		} else if($('#page6').is(":visible")) {
			nextPage = $('#page6').position().top;
		} else {
			nextPage = $('#page5').position().top + $('#page5').height();
		}
		if (nextPage - $('#imageContainer').height() <= scrolPos) {
			$('#imageContainer').hide();
		} else {
			if ($('#systemImage').prop('src') != '' && $('#systemImage').prop('src') != window.location.href) {
				$('#imageContainer').show();
			}
		}
	} else if ($('#' + page2id).position().top <= scrolPos) {
		$('li').removeClass('activeDot');
		$('li').eq(1).addClass('activeDot');
		$('#imageContainer').hide();
	} else {
		$('li').removeClass('activeDot');
		$('li').eq(0).addClass('activeDot');
		$('#imageContainer').hide();
	}
}

$(document).scroll(pagination);

$(document).ready(function () {
	pagination();
	$('.smooth').smoothScroll();
	});

function createNew() {
	page2id = 'page2';
	$('#page2button').prop('href', '#' + page2id);
	$('#page2').show();
	$('#page3').hide();
	$('#page4').hide();
	$('#page2button').click();
	jpeg = null;
	document.getElementById("InVars").value = '';
	document.getElementById("StVarElEqns").value = '';
	document.getElementById("OtherElEqns").value = '';
	document.getElementById("Constraints").value = '';
	document.getElementById("OutputVars").value = '';
	$('#systemImage').prop('src', '');
	$('#page6').hide();
	$('#inputButtons').show();
	$('#page6button').hide();
}

function openExisting() {
	page2id = 'page3';
	$('#page2button').prop('href', '#' + page2id);
	$('#page3').show();
	$('#page2').hide();
	$('#page4').hide();
	$('#page2button').click();
}

function showExamples() {
	page2id = 'page4';
	$('#page2button').prop('href', '#' + page2id);
	$('#page4').show();
	$('#page2').hide();
	$('#page3').hide();
	$('#page2button').click();
}
