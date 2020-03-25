
//<<<FOR BKGND>>>//

//No Distractions Full Screen v4.0
//var scale = 2;
$('#middle').hide()
$('button').hide()

$('body').append(`
<style>

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