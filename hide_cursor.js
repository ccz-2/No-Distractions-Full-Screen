//No Distractions Full Screen v2.3.5
//var cursorIdleTimer = 500; //Defined in python

var cursorHidden = false;
var timer;

function hide_mouse(debug) {
  pycmd("cursor_hide");
  //console.log("cursor_hide: "  + debug);
  //$('*').css({cursor: 'none'});
  cursorHidden = true;
}

function show_mouse(debug) {
  clearTimeout(timer);
  pycmd("cursor_show");
  //console.log("cursor_show: " + debug);
  //$('*').css({cursor: 'default'});
  cursorHidden = false;
}

function countDown(debug) {
  timer = setTimeout(function(){hide_mouse(debug);}, cursorIdleTimer);
}

$(function hide_cursor() {
  if (cursorIdleTimer >= 0) {
    var currentTime = Date.now();
    var lastTime = currentTime;
    countDown('initial')

    $(document).mousemove(function() {
      currentTime = Date.now();
      if (cursorHidden){
        show_mouse('mouse_move_from_hidden');
      } else if (currentTime - lastTime > 500) {
        show_mouse('mouse_move_500ms');
        countDown('stopped_moving')
        lastTime = currentTime; 
      }
    });
  }
});