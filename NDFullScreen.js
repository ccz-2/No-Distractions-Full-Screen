//var op = .5; //Defined in python
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
  background-color: rgba(100, 100, 100, 0.8);
}

body, #outer{
  background: transparent !important;
  border-top-color: transparent !important;
}</style> `);
