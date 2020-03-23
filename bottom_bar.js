//No Distractions Full Screen v4.0
//var op = 0.5; //Defined in python
//var color = 'rgba(110, 110, 200, 0.8)'; //Defined in python
//var sacle = 2;
function getHeight() {
  height = $('table:not([id="innertable"])').height();
  return height
}

$("button[onclick*='edit'],button[onclick*='more']").remove()

$('body').append(`
<style>
table:not([id="innertable"]) {
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

body {
	height:100%;
	width:100%;
}

table#innertable {
  position: absolute;
  left: 0;
  bottom: 0;
}

table {
  border-collapse: collapse;
  empty-cells: hide;
}

</style> `);

function resize(){
    document.body.style.zoom = scale/window.devicePixelRatio;
}
function changeScale(x){ //called from parent
  scale = x;
  resize();
}

window.visualViewport.addEventListener('resize', resize);
window.addEventListener('DOMContentLoaded', resize);