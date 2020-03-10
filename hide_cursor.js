//No Distractions Full Screen v2.3.2
//var cursorIdleTimer = 5000; //Defined in python

var cursorHidden = false;

function hide_mouse() {
  pycmd("cursor_hide");
  console.log("cursor_hide");
  //$('*').css({cursor: 'none'});
  cursorHidden = true;
}

function show_mouse() {
  pycmd("cursor_show");
  console.log("cursor_show");
  //$('*').css({cursor: 'default'});
  cursorHidden = false;
}

$(function hide_cursor() {
  if (cursorIdleTimer >= 0) {
    var currentTime = Date.now();
    var lastTime = currentTime;
    var timer = setTimeout(function(){hide_mouse();}, cursorIdleTimer);

    $(document).mousemove(function() {
      currentTime = Date.now();
      if (cursorHidden){
        show_mouse();
      } else if (currentTime - lastTime > 500) {
        show_mouse();
        clearTimeout(timer);
        timer = setTimeout(function(){hide_mouse();}, cursorIdleTimer);
        lastTime = currentTime; 
      }
      //console.log("skip");
    });
  }
});
