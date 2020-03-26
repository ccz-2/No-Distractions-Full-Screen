//No Distractions Full Screen v4.0
//var op = 0.5; //Defined in python
var newheight;
var newwidth;

$('body').append(`

<style>

#bottomiFrame {
  opacity: ` + op + `;
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
      fitContentDummy();
      iframe.contentWindow.resize()
  });
  observer.observe(target, {
    subtree: true,
    attributes: true,
    childList: true
  });
  fitContent();
  fitContentDummy();
}

function fitContent(){
  var iframe = $('#bottomiFrame')[0]
  var target = iframe.contentDocument.querySelector('table:not([id="innertable"])');
  if (target != null){
    newheight = target.scrollHeight;
    newwidth = target.scrollWidth;
    iframe.height= newheight + 1 + "px";
    iframe.width= newwidth + 1 + "px";
    $("div.bottomWrapper").outerHeight(newheight + 20);
    $("div.bottomWrapper").outerWidth(newwidth);
    resize();
    fitInWindow(); //called from draggable.js
  }
}

function fitContentDummy(){
  var iframe = $('#bottomiFrameBkgnd')[0]
  var target = iframe.contentDocument.body;
  if (target != null){
    newheight = target.scrollHeight;
    newwidth = target.scrollWidth;
    iframe.height= newheight + 1 + "px";
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
  $('#bottomiFrameBkgnd')[0].contentWindow.changeScale(x);
  resize();
}

function activateHover(){
  target = $('#bottomiFrame')[0]
  $(target).css('opacity', op);
  $(target).on({
      mouseenter: function(){
        fade_in();
      },
      mouseleave: function(){
        fade_out()
      },
      touchstart: function(){
        fade_in();
      },
      touchend: function(){
        fade_out()
      }
  });
}

function enable_bottomHover(){
  $("#bottomHover").on({
    mouseenter: function(){
      fade_in();
    },
    mouseleave: function(){
      fade_out();
    }
  });
}

function fade_in(){
  target = $('#bottomiFrame')[0]
  if (!currDrag) { //prevents changes when dragging
    $(target).css('animation-direction','normal');
    $(target).addClass('fade-in');
    $(target).css('opacity','1');
    $(target).on("animationend", function(){
      $(target).removeClass('fade-in');
      });
  }
}

function fade_out(){
  target = $('#bottomiFrame')[0]
  if (currDrag) {
    $(target).removeClass('fade-out');
  }
  else { //prevents changes when dragging
    $(target).css('animation-direction','reverse');
    $(target).addClass('fade-in');
    $(target).css('opacity', op);  
    $(target).on("animationend", function(){
      $(target).removeClass('fade-in');
      });
  }
}