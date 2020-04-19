//No Distractions Full Screen v4.1
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
      resize();
      iframe.contentWindow.resize()
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

function resize(){
  var factor = (window.defaultScale/(window.devicePixelRatio));
  $( ".noZoom" ).each(function() {
    this.style.zoom = (factor);
  });

  resizeDummyFrame()

  if (window.NDAB) {
    fitNDAB();
    return
  }
  var iframe = $('#bottomiFrame')[0]
  var target = iframe.contentDocument.querySelector('table:not([id="innertable"])');
  if (target != null) {
    var factor = (window.devicePixelRatio/window.defaultScale);
    //iframe is fixed to size of bottombar
    $(iframe).css({'height':$('#bottomiFrame')[0].contentWindow.eval('window.innerHeight') * factor});
    $(iframe).css('width',window.innerWidth * factor);

    boundingBox = target.getBoundingClientRect()
    newheight = boundingBox.height
    newwidth = boundingBox.width
    x = boundingBox.x
    y = boundingBox.y
    //pushes iframe contents so that buttons are in top left corner
    $('#bottomiFrame').css({'margin-top':-y,'margin-left':-x});
    //div is wrapped around iframe to show only buttons
    $('div.bottomWrapper').css({'width':newwidth,'height':newheight});
    //resize();
    console.log('iframe:' + iframe.scrollWidth)
    console.log('wrapper:' + $('div.bottomWrapper')[0].scrollWidth)
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
