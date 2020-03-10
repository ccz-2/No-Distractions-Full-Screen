//var op = 0.5; //Defined in python
//var color = 'rgba(110, 110, 200, 0.8)';

$('body').append(`
<script>
var newheight;
var newwidth;

function autoResize(id){
    if(document.getElementById){
        newheight=document.getElementById(id).contentWindow.document .body.scrollHeight;
        newwidth=document.getElementById(id).contentWindow.document .body.scrollWidth;
    }

    newheight = (newheight) + "px"
    newwidth = (newwidth) + "px"
    document.getElementById(id).height= newheight;
    document.getElementById(id).width= newwidth;
};
</script>

<div class="bottomWrapper">
<iframe id='bottomiFrame' frameborder="0" scrolling="no" onLoad="autoResize('bottomiFrame'); test('bottomiFrame')">
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

#bottomiFrame {
  opacity:` + op + `;
  border-radius: 5px;
  background-color: ` + color + `;
}

#bottomiFrame:hover {
  opacity: 1;
}

</style>
`);

