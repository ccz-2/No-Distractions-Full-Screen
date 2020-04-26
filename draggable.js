//No Distractions Full Screen v4.1.6
//Uses interact.js

var target;
var currLock;
var currDrag = false;

function getTarget(){
  target = document.querySelector('div.bottomWrapper');
}

//moves target to within window boundaries
function fitInWindow() {
  if (window.NDAB) {
    return
  }
  setTimeout(function(){ //delay since often called prematurely before target is fully dimensioned
    getTarget()
    if (target !== null && target.getBoundingClientRect().height != 0){
      //debugger;
      var rect = target.getBoundingClientRect();
      var x = parseFloat(target.getAttribute('data-x'));
      var y = parseFloat(target.getAttribute('data-y'));
      windowW = ($("html").prop("clientWidth") * zF()) + 1
      windowH = ($("html").prop("clientHeight") * zF()) + 1
      if (rect.left < 0){
        updatePos(x - rect.left, y);
        x = parseFloat(target.getAttribute('data-x'));
      }
      if (rect.right > windowW) {
        dx = rect.right - windowW;
        updatePos(x - dx , y);
        x = parseFloat(target.getAttribute('data-x'));
      }
      if (rect.top < 0) {
        updatePos(x, y - rect.top);
        y = parseFloat(target.getAttribute('data-y'));
      }
      if (rect.bottom > windowH) {
        dy = rect.bottom - windowH;
        updatePos(x, y - dy );
      }
    }
  },100)
}

function updatePos(x, y){
  getTarget()
  //css transform works in real coordinates (unscaled)
  target.style.transform = 'translate(' + (parseFloat(x) || 0) + 'px, ' + (parseFloat(y) || 0) + 'px)';
  //console.log('translate(' + (parseFloat(x) || 0) + 'px, ' + (parseFloat(y) || 0) + 'px)');
  target.setAttribute("data-x", x);
  target.setAttribute("data-y", y);
  pycmd("NDFS-draggable_pos: " + x + ", " + y);
}

var oldzF = null;
$(window).resize(function() {
  if (oldzF == zF())
  {
    fitInWindow();
  } else {
    oldzF = zF()
  }
});

//Used when toggling off, since screen is redrawn before this javascript is unloaded
function disableResize(){
  $(window).off("resize");
}

function enable_drag(){
  getTarget()
  if (!interact.isSet(target)){
    interact(target).draggable({
      inertia: false,
      enabled: true,
      autoScroll: false,
      onstart: function() {
        currDrag = true;
      },
      onmove: dragMoveListener,
      onend: function (event) {
        var temp = target.getBoundingClientRect();
        //console.log( "pos:" + temp.x + ", " + temp.y);
        fitInWindow();
        var x = event.target.getAttribute('data-x');
        var y = event.target.getAttribute('data-y');
        pycmd("NDFS-draggable_pos: " + x + ", " + y);
        currDrag = false;
      }
    })
  }
  else {
      interact(target).draggable({enabled: true})
  }
  $("#cover").fadeIn(80);
  $(target).css({'box-shadow': '0 19px 38px rgba(0, 0, 0, 0.40), 0 15px 12px rgba(0, 0, 0, 0.25)'});
  currLock = false;
}

// Zoom factor
function zF(){
  return((window.devicePixelRatio)/window.defaultScale)
}

function dragMoveListener(event) {
  var target = event.target
  // keep the dragged position in the data-x/data-y attributes
  var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx * zF();
  var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy * zF();

  // translate the element
  target.style.transform = 'translate(' + x + 'px, ' + y + 'px)'

  // update the posiion attributes
  target.setAttribute('data-x', x)
  target.setAttribute('data-y', y)
}

function disable_drag(){
  getTarget();
  interact(target).unset();
  //interact(target).draggable({enabled: false}); //Will occasionally stop working if disabled - better to unset
  $("#cover").fadeOut(80);
  $(target).css({'-webkit-box-shadow': '', 'border': '', 'background':''});
  currLock = true;
}