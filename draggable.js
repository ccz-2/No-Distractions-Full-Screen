//No Distractions Full Screen v2.

$('table:not([id="innertable"])').draggable({
  containment: "#canvas",
  snap: "#canvas"
});

$( "table:not([id='innertable'])" ).hover(
  function() {
    pycmd('hover_in');
  }, function() {
    pycmd('hover_out');
  }
);