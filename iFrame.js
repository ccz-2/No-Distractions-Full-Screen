//var op = 0.5; //Defined in python
//var color = 'rgba(110, 110, 200, 0.8)';

var newheight;
var newwidth;
function autoResize(id){

};


$('body').append(`

<div class="bottomWrapper">
<iframe id='bottomiFrame' frameborder="0" scrolling="no">
</iframe>
</div>

<style>
.bottomWrapper {
  text-align: center;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
}

</style>
`);

document.querySelector("iframe").addEventListener( "load", function(e) {

    var iframe = e.target
    var target = iframe.contentDocument.querySelector('table:not([id="innertable"])');
    newheight = target.scrollHeight;
    newwidth = target.scrollWidth;
    newheight = (newheight) + "px"
    newwidth = (newwidth) + "px"
    iframe.height= newheight;
    iframe.width= newwidth;
} );