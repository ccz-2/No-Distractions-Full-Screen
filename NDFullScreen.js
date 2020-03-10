//No Distractions Full Screen v2.4
//var op = 0.5; //Defined in python
//var color = 'rgba(110, 110, 200, 0.8)';
console.log("appended")
$('head').append(`
<div id="NDFullScreenInjected"></div>

<style>
html, table {
    height: 0px;
    width: 0px;
    border-width: 0px; 
    border-style: solid;
    border-collapse: collapse;
}

body, #outer{
  background: transparent !important;
  border-top-color: transparent !important;
}</style> `);
$('td.stat').remove()