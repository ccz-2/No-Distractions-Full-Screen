//No Distractions Full Screen v2.3.4
//var cursorIdleTimer = 500; //Defined in python

var cursorHidden = false;
var timer;

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
  clearTimeout(timer);
}

$(function hide_cursor() {
  if (cursorIdleTimer >= 0) {
    var currentTime = Date.now();
    var lastTime = currentTime;
    timer = setTimeout(function(){hide_mouse();}, cursorIdleTimer);

    $(document).mousemove(function() {
      currentTime = Date.now();
      if (cursorHidden){
        show_mouse();
      } else if (currentTime - lastTime > 500) {
        show_mouse();
        timer = setTimeout(function(){hide_mouse();}, cursorIdleTimer);
        lastTime = currentTime; 
      }
      //console.log("skip");
    });
  }
});

//Needed when adding card - not activated by hook
$(function test() {
  var focused = false
  setInterval(function(){ loseFocus(); }, 200);
  function loseFocus() {
    if (!document.hasFocus()) {
      if (focused) {
        show_mouse();
        focused = false}
    } else {
    focused = true;
    }
  }
});

//removes timers when leaving element
$(document).mouseleave(function () {
  show_mouse();
});
