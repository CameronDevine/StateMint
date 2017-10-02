var page2id = 'page2';

function pagination() {
	var scrolPos = $(document).scrollTop();
	if ($('#page6').position().top <= scrolPos) {
		$('li').removeClass('activeDot');
		$('li').eq(3).addClass('activeDot');
	} else if ($('#page5').position().top <= scrolPos) {
		$('li').removeClass('activeDot');
		$('li').eq(2).addClass('activeDot');
	} else if ($('#' + page2id).position().top <= scrolPos) {
		$('li').removeClass('activeDot');
		$('li').eq(1).addClass('activeDot');
	} else {
		$('li').removeClass('activeDot');
		$('li').eq(0).addClass('activeDot');
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
