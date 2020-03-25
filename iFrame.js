//No Distractions Full Screen v4.0
//var op = 0.5; //Defined in python
var newheight;
var newwidth;

$('body').append(`

<style>

.bottomWrapper {
  opacity: ` + op + `
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

//Queued from python after _initWeb and _showAnswer/_showQuestion scripts are queued 
function finishedLoad(){
  var iframe = $('#bottomiFrame')[0]
  var target = iframe.contentDocument.getElementById('middle')
  var observer = new MutationObserver(function(mutations, observer) {
      fitContent()
      iframe.contentWindow.resize()
  });
  observer.observe(target, {
    subtree: true,
    attributes: true,
    childList: true
  });
  fitContent();
}

function monitorContent(){
  var iframe = $('#bottomiFrame')[0].contentDocument
  var observer = new MutationObserver(function(mutations, observer) {
      console.log(mutations)
  });
  observer.observe(iframe, {
    subtree: true,
    attributes: true,
    childList: true
  });
}

function fitContent(){
  var iframe = $('#bottomiFrame')[0]
  var target = iframe.contentDocument.querySelector('table:not([id="innertable"])');
  if (target != null){
    newheight = target.scrollHeight;
    newwidth = target.scrollWidth;
    iframe.height= newheight + "px";
    iframe.width= newwidth + "px";
    $("div.bottomWrapper").outerHeight(newheight + 20);
    $("div.bottomWrapper").outerWidth(newwidth);
    resize();
    fitInWindow(); //called from draggable.js
  }
}

function resize(){
  var factor = (window.defaultScale/(window.devicePixelRatio));
  $('#outer')[0].style.zoom = (factor);
}

window.visualViewport.addEventListener('resize', resize);

function changeScale(x) { //Adjusts to new scale e.g. changing screen DPI; calls iFrame function to update scale
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