//No Distractions Full Screen v3.3

function getHeight() {
  height = $('table:not([id="innertable"])').height();
  return height
}

$("button[onclick*='edit'],button[onclick*='more']").remove()
$('body').wrap(`<div id="canvas"></div>`)
$('body').append(`<div id="bottomHover"></div>`)