//No Distractions Full Screen v3.2
//var cursorIdleTimer = 500; //Defined in python

var cursorHidden = false;
var timer;

function hide_mouse(debug) {
  pycmd("NDFS-cursor_hide");
  //console.log("NDFS-cursor_hide: "  + debug);
  cursorHidden = true;
}

function show_mouse(debug) {
  clearTimeout(timer);
  pycmd("NDFS-cursor_show");
  //console.log("NDFS-cursor_show: " + debug);
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