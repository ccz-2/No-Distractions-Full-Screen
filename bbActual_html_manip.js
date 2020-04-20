
//<<<FOR ACTUAL>>>//

//No Distractions Full Screen v4.1.3

$('table:not([id="innertable"])').parents().siblings().hide()
$('td.stat').hide()

$('body').append(`
<style>
table:not([id="innertable"]) {
  background-color: transparent !important;
}

body, #outer{
  background: transparent !important;
  border-top-color: transparent !important;
}

</style> `);