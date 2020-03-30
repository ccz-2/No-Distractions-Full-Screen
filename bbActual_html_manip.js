
//<<<FOR ACTUAL>>>//

//No Distractions Full Screen v4.0
//var color = 'rgba(110, 110, 200, 0.8)'; //Defined in python

$('table:not([id="innertable"])').parents().siblings().hide()
$('td.stat').hide()

$('body').append(`
<style>
table:not([id="innertable"]) {
  position: absolute;
  z-index: 999;
  padding: 0px;
  background-color: ` + color + `;
  user-select: none;
  vertical-align: bottom;
}

body, #outer{
  background: transparent !important;
  border-top-color: transparent !important;
  overflow: hidden;
  margin: 0;
}

</style> `);