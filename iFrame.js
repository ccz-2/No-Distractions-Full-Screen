//var op = 0.5; //Defined in python
//var color = 'rgba(110, 110, 200, 0.8)';
//var topBar = 15;
//var defaultZoom = 2;

$('body').append(`

<script>
function resize(){
    document.getElementById('bottomiFrame').style.zoom = (` + defaultZoom + `/(window.devicePixelRatio));
    console.log('iFrame Parent Zoom:' + document.getElementById('bottomiFrame').style.zoom);
    pycmd("NDFS: Resized");
}

window.visualViewport.addEventListener('resize', resize);

var pointerX;
var pointerY;
var zoom = window.devicePixelRatio/` + defaultZoom + `;

//$('#bottomiFrame').draggable({
//  start : function(evt, ui) {
//    pointerY = (evt.pageY - $('#canvas').offset().top) / zoom - parseInt($(evt.target).css('top'));
//    console.log($('#canvas').offset().top)
//    pointerX = (evt.pageX - $('#canvas').offset().left) / zoom - parseInt($(evt.target).css('left'));
//  },
//  drag : function(evt, ui) {
//    var canvasTop = $('#canvas').offset().top;
//    var canvasLeft = $('#canvas').offset().left;
//    var canvasHeight = $('#canvas').height();
//    var canvasWidth = $('#canvas').width();
//
//    // Fix for zoom
//    ui.position.top = Math.round((evt.pageY - canvasTop) / zoom - pointerY); 
//    ui.position.left = Math.round((evt.pageX - canvasLeft) / zoom - pointerX); 
//
// 
//
//    // Finally, make sure offset aligns with position
//    ui.offset.top = Math.round(ui.position.top + canvasTop);
//    ui.offset.left = Math.round(ui.position.left + canvasLeft);
//  }
//});

$('#bottomiFrame').draggable({
      containment: "#canvas",
      snap: "#canvas",
//    iframeFix: true
//    drag : function(evt, ui) {
//    $( "#bottomiFrame" ).draggable({ handle: "#canvas" });
//    }
});

</script>

<script>
var topBar = `+ topBar +`;
var zoomFactor;
function autoResize(id){
    var radius = 5;
    console.log(topBar);
    if(document.getElementById){
        newheight=document.getElementById(id).contentWindow.document.body.scrollHeight;
        newwidth=document.getElementById(id).contentWindow.document.body.scrollWidth;
    }
    //zoomFactor = ` + defaultZoom + `/document.getElementById('bottomiFrame').contentWindow.devicePixelRatio;
    zoomFactor = 1;
    newheight = (newheight*zoomFactor) + "px";
    newwidth = (newwidth*zoomFactor) + "px";
    newtopBar = (topBar*zoomFactor) + "px";
    newradius = (radius*zoomFactor) + "px";
    document.getElementById(id).height= newheight;
    document.getElementById(id).width= newwidth;
    document.documentElement.style.setProperty('--topBar', newtopBar);
    document.documentElement.style.setProperty('--radius', newradius);
    console.log("Height: " + newheight + " Width: " + newwidth); // + " ZoomFactor: " + zoomFactor);
    //resize();
};
</script>

<div class="bottomWrapper">
<iframe id='bottomiFrame' frameborder="0" scrolling="no" onLoad="autoResize('bottomiFrame');">
</iframe>
</div>
<div id="canvas"></div>

<style>

:root {
  --topBar: 20px;
  --radius: 5px;
}

#canvas {
    position: fixed;
    width:100%;
    height:100%;
    top: 0px;
    left: 0px;
    z-index: -999;
    background-color: red;
}

.bottomWrapper {
  padding: 0px;
  margin: 0px;
  height: auto;
  text-align: center;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;

}

#bottomiFrame {
  opacity:` + op + `;
  border-radius: var(--radius);
  padding-top: var(--topBar);
  background: linear-gradient(to bottom, #023 var(--topBar), transparent var(--topBar));
  background-color: ` + color + `;
  user-select: none;
  vertical-align: bottom;

}

#bottomiFrame:hover {
  opacity: 1;
}

</style>

`);

