//var url = '';
var defaultZoom = 2;

url = decodeURIComponent(url);

mouseMove = `<script>
$(function hide_mouse_move() {
    $(document).mousemove(function() {
        moving();})
});
function pycmd(a){parent.pycmd(a)};
function moving(){parent.moving()};

function resize (){
    document.body.style.zoom = ` + defaultZoom + `/window.devicePixelRatio;
    console.log('iFrame zoom: '+ document.body.style.zoom)
}

window.visualViewport.addEventListener('resize', resize);
</script>

<style>
* {
  user-select: none;
}
</style>
`;

//executes in iFrame
$(document).ready(function(){
    $("#bottomiFrame").attr("srcdoc", url+mouseMove);
});
