function pagination() {
	var scrolPos = $(document).scrollTop();
	if ($('#page5').position().top <= scrolPos) {
		$('li').removeClass('activeDot');
		$('li').eq(4).addClass('activeDot');
	} else if ($('#page4').position().top <= scrolPos) {
		$('li').removeClass('activeDot');
		$('li').eq(3).addClass('activeDot');
	} else if ($('#page3').position().top <= scrolPos) {
		$('li').removeClass('activeDot');
		$('li').eq(2).addClass('activeDot');
	} else if ($('#page3').position().top <= scrolPos) {
		$('li').removeClass('activeDot');
		$('li').eq(2).addClass('activeDot');
	} else if ($('#page2').position().top <= scrolPos) {
		$('li').removeClass('activeDot');
		$('li').eq(1).addClass('activeDot');
	}  else {
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
	$('#page2').show();
	$('#page3').hide();
	$('#page2button').click();
}

function openExisting() {
	$('#page3').show();
	$('#page2').hide();
	$('#page3button').click();
}

function startOver() {
	var a = document.createElement('a');
	a.href = "#page1";
	a.click();
}
