// NDFS v3.3

var newheight;
var newwidth;

$('body').append(`
<div id="outer">
<div class="bottomWrapper">
<iframe id='bottomiFrame' frameborder="0" scrolling="no">
</iframe>
</div>
</div>

<style>

#outer{
  right: 0;
  bottom: 0;
  position: fixed;
  left: 50%;
  height: auto;
  background-color: green;
}

.bottomWrapper {
  position: relative;
  left: -50%;
  background-color: red;
  margin: 0px;
}

</style>
`);

/*
.bottomWrapper {
  text-align: center;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
}
*/

document.querySelector("iframe").addEventListener( "load", function(e) {
    var iframe = e.target
    var target = iframe.contentDocument.querySelector('table:not([id="innertable"])');
    newheight = target.scrollHeight;
    newwidth = target.scrollWidth;
    newheight = (newheight) + "px"
    newwidth = (newwidth) + "px"
    iframe.height= newheight;
    iframe.width= newwidth;
    $("div.bottomWrapper").outerHeight(newheight + 50);
    $("div.bottomWrapper").outerWidth(newwidth);

} );
