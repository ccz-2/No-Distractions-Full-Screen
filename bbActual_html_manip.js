
//<<<FOR ACTUAL>>>//

//No Distractions Full Screen v4.1.7

$('table:not([id="innertable"])').parents().siblings().hide()
$('td.stat').hide()

$('body').append(`
<style>

table:not([id="innertable"]) {
  //border-color: coral;
  //border-style: solid;
  background-color: transparent !important;
  position: absolute;
  left: 0;
  bottom: 0;
  padding: 0px;
}

body, #outer{
  background: transparent !important;
  border-top-color: transparent !important;
  overflow: hidden;
}

</style> `);