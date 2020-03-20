//No Distractions Full Screen v3.2
//Uses interact.js

var target;
var currLock;
var currDrag = false;

function getTarget(){
  target = document.querySelector('div.bottomWrapper');
}

//moves target to within window boundaries
function fitInWindow() {
  getTarget()
  if (target !== null){
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
}

$(window).resize(function() {
  fitInWindow();
});

function updatePos(x, y){
  getTarget()
  //css transform works in real coordinates (unscaled)
  target.style.transform = 'translate(' + (parseFloat(x) || 0) + 'px, ' + (parseFloat(y) || 0) + 'px)';
  target.setAttribute("data-x", x);
  target.setAttribute("data-y", y);
}

function getOrigPos() { //recursively calculates target original position (before transform)
  var el = target, offsetLeft = 0, offsetTop  = 0;
  do{
      offsetLeft += el.offsetLeft;
      offsetTop  += el.offsetTop;
      el = el.offsetParent;
  } while( el );
  console.log(offsetLeft + ":" + offsetTop + ":" + 50/zF())
  return {
    x: offsetLeft, //snap target
    y: offsetTop,
    range: 50/zF(), //snap 'stickiness'
  }
}

function enable_drag(){
  getTarget()
  fitInWindow()
  if (!interact.isSet(target)){
    interact(target).draggable({
      inertia: false,
      enabled: true,
      autoScroll: false,
      modifiers: [
        interact.modifiers.snap({
          targets: [getOrigPos()],
          relativePoints: [ { x: 0, y: 0} ] //snap to top-left
          })],
      onstart: function() {
        currDrag = true;
      },
      onmove: dragMoveListener,
      onend: function (event) {
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
  $(target).css({'-webkit-box-shadow': '0 0 10px LightBlue'});
  currLock = false;
}

// Zoom factor
function zF(){
  return((window.devicePixelRatio)/window.defaultScale)
}

function dragMoveListener (event) {
  var target = event.target
  // keep the dragged position in the data-x/data-y attributes
  var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx * zF();
  var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy * zF();

  // translate the element
  target.style.webkitTransform =
    target.style.transform =
      'translate(' + x + 'px, ' + y + 'px)'

  // update the posiion attributes
  target.setAttribute('data-x', x)
  target.setAttribute('data-y', y)
}

function disable_drag(){
  getTarget();
  fitInWindow();
  interact(target).unset();
  //interact(target).draggable({enabled: false}); //Will occasionally stop working if disabled - better to unset
  $(target).css({'-webkit-box-shadow': '', 'border': ''});
  currLock = true;
}

var mousedown = false;
function activateHover(){
  getTarget();
  $(target).on({
      mouseenter: function(){
        fade_in(target);
      },
      mouseleave: function(){
        fade_out(target)
      },
      touchstart: function(){
        fade_in(target);
      },
      touchend: function(){
        fade_out(target)
      }
  });
}

function enable_bottomHover(){
  getTarget();
  $("#bottomHover").on({
    mouseenter: function(){
      fade_in(target);
    },
    mouseleave: function(){
      fade_out(target);
    }
  });
}

function fade_in(target){
  if (!currDrag) { //prevents changes when dragging
    $(target).css('animation-direction','normal');
    $(target).addClass('fade-in');
    $(target).css('opacity','1');  
    $(target).on("animationend", function(){
      $(this).removeClass('fade-in');
      });
  }
}

function fade_out(target){
  if (!currDrag) { //prevents changes when dragging
    $(target).css('animation-direction','reverse');
    $(target).addClass('fade-in');
    $(target).css('opacity','');  
    $(target).on("animationend", function(){
      $(this).removeClass('fade-in');
      });
  }
}