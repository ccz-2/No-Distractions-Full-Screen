//No Distractions Full Screen v3.3

$('body').wrap(`<div id="canvas"></div>`)
$('body').append(`<div id="bottomHover"></div>`)

//pretty bad - should not inject
var timer;
$("body").on('DOMSubtreeModified', 'td#middle', function() {
	$('table:not([id="innertable"])').addClass("bar");
	if (!$('table.bar td div').hasClass('again')) {
		$('button:contains("Again")').closest('td').append('<div class="again"></div>')
		$('button:contains("Again")').remove()
	}
	if (!$('table.bar td div').hasClass('hard')) {
		$('button:contains("Hard")').closest('td').append('<div class="hard"></div>')
		$('button:contains("Hard")').remove()
	}
	if (!$('table.bar td div').hasClass('good')) {
		$('button:contains("Good")').closest('td').append('<div class="good"></div>')
		$('button:contains("Good")').remove()
	}
	if (!$('table.bar td div').hasClass('easy')) {
		$('button:contains("Easy")').closest('td').append('<div class="easy"></div>')
		$('button:contains("Easy")').remove()
	}
	if (!$('table.bar td div').hasClass('ans')){
		$('button:contains("Show Answer")').closest('td').append('<div class="ans"></div>')
		$('button:contains("Show Answer")').remove()
	}
	$('button').remove()
});

$("body").on('DOMContentLoaded', function() {
	console.log(event.target)
});

function getHeight() {
  height = $('table:not([id="innertable"])').height();
  return height
}