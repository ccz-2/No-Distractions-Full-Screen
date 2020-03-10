//No Distractions Full Screen v2.3.3
//var op = 0.5; //Defined in python
//var color = 'rgba(110, 110, 200, 0.8)';
//console.log("appended")
$("button[onclick*='edit'],button[onclick*='more']").remove()

$('body').append(`
<div id="canvas"></div>
<style>
table:not([id="innertable"]):hover {
  opacity: 1;
}

table:not([id="innertable"]) {
  opacity:` + op + `;
  padding: 0px;
  border-radius: 5px;
  background-color: ` + color + `;
  user-select: none;
  vertical-align: bottom;
}

body, #outer{
  background: transparent !important;
  border-top-color: transparent !important;
  overflow: hidden; /* Hide scrollbars */
}

body {
	//height:500px;
}

/*td#middle {
height: 100vh;
}*/

table {
  border-collapse: collapse;
  empty-cells: hide;
}

#canvas {
    position: absolute;
    width:100vw;
    height:100vh;
    top: 0px;
    left: 0px;
    z-index: -999;
    //background-color: red;
}
</style> `);
