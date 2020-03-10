//No Distractions Full Screen v2.4
//var op = 0.5; //Defined in python
//var color = 'rgba(110, 110, 200, 0.8)';
//console.log("appended")
$("button[onclick*='edit'],button[onclick*='more']").remove()
$('head').append(`
<div id="NDFullScreenInjected"></div>

<script>
function getMinWidth() {
	var table = document.getElementById('innertable');
	// get the original width in case it was set
	var originalWidth = table.style.width;
	// set the table's width to 1px (0 does not work)
	table.style.width = '1px';
	// get the current width
	var smallestWidth = table.getBoundingClientRect().width;
	// set the original width back 
	table.style.width = originalWidth;
	return(smallestWidth);
}
</script>

<style>
table:not([id="innertable"]):hover {
  opacity: 1;
}

table:not([id="innertable"]) {
  opacity:` + op + `;
  padding: 0px;
  border-radius: 5px;
  background-color: ` + color + `;  
}

body, #outer{
  background: transparent !important;
  border-top-color: transparent !important;
}

table {
  border-collapse: collapse;
  empty-cells: hide;
}
</style> `);
