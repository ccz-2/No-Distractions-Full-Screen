//No Distractions Full Screen v4.0
//var op = 0.5; //Defined in python
var newheight;
var newwidth;

$('body').append(`
  <div id='outer'>
    <div class="bottomWrapper">
      <iframe id='bottomiFrame' frameborder="0" scrolling="no">
      </iframe>
    </div>
  </div>

<div id='bottomHover'></div>

<style>
#bottomHover {
    position: fixed;
    width:100%;
    height: 15px;
    bottom: 0px;
    left: 0px;
    //background-color: red;
}

#outer{
  bottom: 0;
  position: fixed;
  left: 50%;
  //background-color: green;
}

.bottomWrapper {
  position: relative;
  left: -50%;
  //background-color: red;
  border-radius: 5px;
  margin: 0px;
  pointer-events: auto;
  //touch-action: none;
  opacity: ` + op + `
  user-select: none;
}

#canvas{
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  margin: 0px;
  pointer-events: none;
  background-color: teal;
}

#bottomiFrame {
  display:block;
  margin: 0px;
  position: absolute;
  bottom: 0;
  user-select: none;
}

.fade-in {
  animation-name: fadeInOpacity;
  animation-iteration-count: 1;
  animation-timing-function: ease-in-out;
  animation-duration: 0.15s;
}

@keyframes fadeInOpacity {
  0% {
    opacity: ` + op + `;
  }
  100% {
    opacity: 1;
  }
}

</style>
`);

$('#bottomiFrame')[0].addEventListener( "load", function(e){
  var iframe = e.target
  var target = iframe.contentDocument.querySelector('table:not([id="innertable"])');
  newheight = target.scrollHeight;
  newwidth = target.scrollWidth;
  iframe.height= newheight + "px";
  iframe.width= newwidth + "px";
  $("div.bottomWrapper").outerHeight(newheight + 20);
  $("div.bottomWrapper").outerWidth(newwidth);
  resize();
  fitInWindow();
});

function resize(){
  var factor = (window.defaultScale/(window.devicePixelRatio));
  $('#outer')[0].style.zoom = (factor);
}

window.visualViewport.addEventListener('resize', resize);

function changeScale(x) { //Adjusts to new scale, calls iFrame function to update scale
  window.defaultScale = x;
  $('#bottomiFrame')[0].contentWindow.changeScale(x);
  resize();
}

var mousedown = false;
function activateHover(){
  target = document.querySelector('div.bottomWrapper');
  $(target).css('opacity', op);  
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
  target = document.querySelector('div.bottomWrapper');
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
  if (currDrag) {
    $(this).removeClass('fade-out');
  }
  else { //prevents changes when dragging
    $(target).css('animation-direction','reverse');
    $(target).addClass('fade-in');
    $(target).css('opacity', op);  
    $(target).on("animationend", function(){
      $(this).removeClass('fade-in');
      });
  }
}