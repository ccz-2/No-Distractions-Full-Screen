//No Distractions Full Screen v3.3

$('body').wrap(`<div id="canvas"></div>`)
$('body').append(`<div id="bottomHover"></div>`)

//pretty bad - should not inject
var timer;
$("body").on('DOMSubtreeModified', 'td#middle', function() {
  clearTimeout(timer);
  timer = setTimeout(function(){
	$('table:not([id="innertable"])').addClass("bar");
	$('button[data-ease="1"]').closest('td').addClass('asdf').append('<div class="again"></div>')
	$('button[data-ease="2"]').closest('td').addClass('asdf').append('<div class="hard"></div>')
	$('button[data-ease="3"]').closest('td').addClass('asdf').append('<div class="good"></div>')
	$('button[data-ease="4"]').closest('td').addClass('asdf').append('<div class="easy"></div>')
	$("button").remove()
  }, 10); //prevents overzealous updates, since selector grabs multiple events per card change
});


function getHeight() {
  height = $('table:not([id="innertable"])').height();
  return height
}