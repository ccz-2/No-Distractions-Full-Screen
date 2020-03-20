// NDFS v3.3

var newheight;
var newwidth;

$('body').append(`
  <div id='outer'>
    <div class="bottomWrapper">
      <iframe id='bottomiFrame' frameborder="0" scrolling="no">
      </iframe>
    </div>
  </div>
<style>

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
  touch-action: none;
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
    resize()
} );

function resize(){
  var factor = (2/(window.devicePixelRatio));
  $('#outer')[0].style.zoom = (factor);
  //$('#outer')[0].style.transform = "scale("+ factor +", " + factor + ")";    
}

window.visualViewport.addEventListener('resize', resize);