//No Distractions Full Screen v2.3.3
//var op = 0.5; //Defined in python
//var color = 'rgba(110, 110, 200, 0.8)';
console.log("appended")
$('head').append(`
<div id="NDFullScreenInjected"></div>

<style>
table:not([id="innertable"]){
  opacity:` + op + `;
}

table:not([id="innertable"]):hover {
  opacity: 1;
}

button[onclick*="edit"],
button[onclick*="more"] {
  visibility: hidden;
}

table:not([id="innertable"]) {
  padding: 0px;
  border-radius: 5px;
  background-color: ` + color + `; 
}

body, #outer{
  background: transparent !important;
  border-top-color: transparent !important;
}</style> `);
