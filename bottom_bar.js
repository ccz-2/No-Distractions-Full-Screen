//No Distractions Full Screen v3.2.2
//var op = 0.5; //Defined in python
//var color = 'rgba(110, 110, 200, 0.8)'; //Defined in python

function getHeight() {
  height = $('table:not([id="innertable"])').height();
  return height
}

$("button[onclick*='edit'],button[onclick*='more']").remove()

$('body').append(`
<style>
table:not([id="innertable"]) {
  opacity:` + op + `;
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

.fade-in {
  animation-name: fadeInOpacity;
  animation-iteration-count: 1;
  animation-timing-function: ease-in-out;
  animation-duration: 0.2s;
}

@keyframes fadeInOpacity {
  0% {
    opacity: ` + op + `;
  }
  100% {
    opacity: 1;
  }
}

</style> `);
