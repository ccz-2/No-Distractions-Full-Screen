//<<<FOR ACTUAL>>>//
//No Distractions Full Screen v4.0
//var op = 0.5; //Defined in python
//var color = 'rgba(110, 110, 200, 0.8)'; //Defined in python
//var scale = 2;

$('table:not([id="innertable"])').parents().siblings().hide()
$('td.stat').hide()

$('body').append(`
<style>
table:not([id="innertable"]) {
  position: absolute;
  left: 0;
  bottom: 0;
  z-index: 999;
  padding: 0px;
  border-radius: 5px;
  background-color: ` + color + `;
  user-select: none;
  touch-action: none;
  vertical-align: bottom;
}

body, #outer{
  background: transparent !important;
  border-top-color: transparent !important;
  overflow: hidden;
}

</style> `);

//Called from resize events and mutation observer in parent
function resize(){
    document.body.style.zoom = scale/window.devicePixelRatio;
}

function changeScale(x){ //called from parent
  scale = x;
  resize();
}
function getHeight() {
  height = $('table:not([id="innertable"])').height();
  return height
}

window.visualViewport.addEventListener('resize', resize);