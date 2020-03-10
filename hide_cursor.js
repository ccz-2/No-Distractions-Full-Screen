//No Distractions Full Screen v2.4
//var cursorIdleTimer = 5000; //Defined in python

var cursorHidden = false;
var timer;

function hide_mouse(debug) {
    //console.log("NDFS hide: "+debug);
    pycmd("NDFS hide: "+debug);
    //$('*').css({cursor: 'none'});
    cursorHidden = true;
}

function show_mouse(debug) {
    //console.log("NDFS show: "+debug);
    pycmd("NDFS show: "+debug);
    //$('*').css({cursor: 'default'});
    cursorHidden = false;
    clearTimeout(timer);
    timer = setTimeout(function(){hide_mouse(debug);}, cursorIdleTimer);
}

$(function hide_mouse_move() {
    $(document).mousemove(function() {
        moving();})
});

var currentTime = Date.now();
var lastTime = currentTime;
show_mouse('start');
function moving() {
    if (cursorIdleTimer >= 0) {
        currentTime = Date.now();
        if (cursorHidden){
            show_mouse('move');
        } else if (currentTime - lastTime > 500) {
            show_mouse('moving');
            lastTime = currentTime; 
        }
    }
}

//Needed when adding card - not activated by hook
$(function hide_lose_focus() {
    var focused = false
    var count = 1;
    setInterval(function(){ loseFocus(); }, 100);
    function loseFocus() {
        if (document.hasFocus()) {
            if (!focused) {
                show_mouse('hasFocus');
                focused = true
                }
        } else {
            if (focused) {
                show_mouse('loseFocus');
                clearTimeout(timer);
                focused = false;
            }
        }
    }
});

//removes timers when leaving element
$(document).mouseleave(function () {
  show_mouse('mouseLeave');
  clearTimeout(timer);
});
