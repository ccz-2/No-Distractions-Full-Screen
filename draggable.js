//No Distractions Full Screen v3.2
//Uses interact.js

var target;
var currX;
var currY;
var currLock;
var currHover;
var currDrag = false;

function getTarget(){
  target = document.querySelector('div.bottomWrapper');
}

/*/called when screen updates
var timeout = false;
$("body").on('DOMSubtreeModified', 'td#middle', function() {
  getTarget();
  if(target != null && !timeout){
    timeout = true;
    updatePos(currX, currY);
    activateHover();
    if (currLock){
      disable_drag();
    }
    else {
      enable_drag();    
    }
    if (currHover){
      fade_in(target);
    }
    setTimeout(function(){ timeout = false; }, 5); //prevents overzealous updates, since selector grabs multiple events per card change
  }
});*/

//moves target to within window boundaries
function fitInWindow() {
  getTarget()
  if (target !== null){
    var rect = target.getBoundingClientRect();
    var x = parseFloat(target.getAttribute('data-x'));
    var y = parseFloat(target.getAttribute('data-y'));
    windowW = $("html").prop("clientWidth") * zF()
    windowH = $("html").prop("clientHeight") * zF()
    if (rect.x < 0){
      updatePos(x - rect.x, y)
    }
    if (rect.right > windowW){
      dx = rect.right - windowW
      updatePos(x - dx , y)
    }
    if (rect.top < 0){
      updatePos(x, y - rect.top)
    }
    if (rect.bottom > windowH){
      dy = rect.bottom - windowH
      updatePos(x, y - dy )
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
  currX = x;
  currY = y;
}

function restrictBBox() {
  bbox = $('#canvas')[0].getBoundingClientRect();
  bbox.bottom = bbox.bottom * zF();
  bbox.height = bbox.height * zF();
  bbox.right = bbox.right * zF(); 
  bbox.width = bbox.width * zF();
  console.log('asdf')
  return bbox
}

function enable_drag(){
  getTarget()
  fitInWindow()
  if (!interact.isSet(target)){
    interact(target).draggable({
      inertia: true,
      enabled: true,
      modifiers: [
          interact.modifiers.restrictRect({
            restriction: restrictBBox(),
            endOnly: true
          })/*,
            interact.modifiers.snap({
              targets: [
            function () { //recursively calculates target original position (before transform)
            var el = target, offsetLeft = 0, offsetTop  = 0;
            do{
                offsetLeft += el.offsetLeft;
                offsetTop  += el.offsetTop;
                el = el.offsetParent;
            } while( el );
              return {
                x: offsetLeft * zF(), //snap target
                y: offsetTop * zF(),
                range: 50, //snap 'stickiness'
              }
            }
              ],
            relativePoints: [
            { x: 0, y: 0} //snap to top-left
          ]
            })*/
      ],
      autoScroll: false,
      onstart: function() {
        currDrag = true;
        interact(target).draggable({modifiers: interact.modifiers.restrictRect({restriction: restrictBBox(), endOnly:true})})
      },
      onmove: dragMoveListener,
      onend: function (event) {
        var x = event.target.getAttribute('data-x');
        var y = event.target.getAttribute('data-y');
        pycmd("NDFS-draggable_pos: " + x + ", " + y);
        currX = x;
        currY = y;
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
  return((window.devicePixelRatio)/2)
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
    currHover = true;
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
    currHover = false;
  }
}