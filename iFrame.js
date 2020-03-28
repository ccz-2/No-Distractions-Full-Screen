//No Distractions Full Screen v4.0
//var op = 0.5; //Defined in python

var newheight;
var newwidth;

$('body').append(`

<style>

#bottomiFrame {
  opacity: `+op+`;
  transition: 0.15s;
}

#bottomiFrame:hover {
  opacity: 1;
}
</style>
`);

//Queued from python after _initWeb and _showAnswer/_showQuestion scripts are queued 
function finishedLoad(){
  var iframe = $('#bottomiFrame')[0]
  if (window.NDAB) {
    var target = iframe.contentDocument.getElementById('container')    
  }
  else {
    var target = iframe.contentDocument.getElementById('middle')    
  }
  var observer = new MutationObserver(function(mutations, observer) {
      fitContent()
      fitContentDummy();
      resize();
      iframe.contentWindow.resize()
  });
  observer.observe(target, {
    subtree: true,
    attributes: true,
    childList: true
  });
  fitContent();
  fitContentDummy();
  resize();
}

function fitContent(){
  if (window.NDAB) {
    fitNDAB();
    return
  }
  else {
    var iframe = $('#bottomiFrame')[0]
    var target = iframe.contentDocument.querySelector('table:not([id="innertable"])');
  }
  if (target != null) {
    newheight = target.scrollHeight + 1;
    newwidth = target.scrollWidth + 1;
    iframe.height = newheight + "px";
    iframe.width = newwidth + "px";
    $("div.bottomWrapper").outerHeight(newheight);
    $("div.bottomWrapper").outerWidth(newwidth);
    resize();
    if (!window.NDAB) {
      fitInWindow(); //called from draggable.js
    }
  }
}

function fitContentDummy(){
  var iframe = $('#bottomiFrameBkgnd')[0]
  var target = iframe.contentDocument.body;
  if (target != null){
    newheight = target.scrollHeight;
    iframe.height= newheight + 1 + "px";
  }
}

function fitNDAB(){
  var iframe = $('#bottomiFrame')[0]
  var target = iframe.contentDocument.body;
  if (target != null){
    newheight = target.scrollHeight;
    iframe.height= newheight + "px";
    $("div.bottomWrapper").outerHeight(newheight);
    $("div.bottomWrapper").css({'position':'fixed','left':'0','bottom':'0','width':'100%'});
    $(iframe).css('width','100%');
    $("div.bottomWrapper")[0].style.transform = 'translate(0px, 0px)'
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

function enable_bottomHover(){
  $("body").append(`<style>
    #bottomHover:hover #bottomiFrame{
      opacity: 1;
    }</style>`);
  $("#bottomHover").css(`pointer-events`,'auto');
}