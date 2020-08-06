//No Distractions Full Screen v4.1.7
//var op = 0.5; //Defined in python

var newheight;
var newwidth;

$('body').append(`

<style>

#bottomiFrame {
  opacity: `+op+`;
  transition-duration: 0.15s;
  transition-property: opacity;
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
      iframe.contentWindow.resize() //must be before resize to get correct bounding box coords
      resize();
  });
  observer.observe(target, {
    subtree: true,
    attributes: true,
    childList: true
  });
  resize();
}

function resizeDummyFrame(){
  var iframe = $('#bottomiFrameBkgnd')[0]
  var target = iframe.contentDocument.body;
  if (target != null){
    newheight = target.scrollHeight;
    iframe.height= newheight + "px";
  }
}

function fitNDAB(){
  var iframe = $('#bottomiFrame')[0]
  var target = iframe.contentDocument.body;
  var factor = (window.devicePixelRatio/window.defaultScale);
  if (target != null){
    newheight = target.scrollHeight;
    iframe.height= newheight + "px";
    $("div.bottomWrapper").outerHeight(newheight);
    $(iframe).css('width',window.innerWidth * factor);
    $("div.bottomWrapper")[0].style.transform = 'translate(0px, 0px)'
  }
}

var oldZoom;
function resize(){

  var factor = (window.defaultScale/(window.devicePixelRatio));
  $( ".noZoom" ).each(function() {
    this.style.zoom = (factor);
  });

  if (factor != oldZoom) { //resize is a zoom event, skip iframe adjustment
    oldZoom = factor;
    return
  }

  resizeDummyFrame()

  if (window.NDAB) {
    fitNDAB();
    return
  }

  var iframe = $('#bottomiFrame')[0]
  var target = iframe.contentDocument.querySelector('table:not([id="innertable"])');

  if (target != null) {
    //iframe is fixed to size of window
    var refBB = $('#bottomiFrameBkgnd')[0].contentDocument.querySelector('table:not([id="innertable"])').getBoundingClientRect();
    $(iframe).css('width',refBB.width)

    boundingBox = target.getBoundingClientRect()
    newheight = boundingBox.height
    newwidth = boundingBox.width
    x = boundingBox.x
    y = boundingBox.y

    //iframe is cropped to only show target
    $('div.bottomWrapper').css({'width':newwidth,'height':newheight}); 
    $('#bottomiFrame').css({'top':-y,'left':-x});
  }
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
