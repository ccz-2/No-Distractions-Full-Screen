//var url = '';
url = decodeURIComponent(url);

mouseMove = `<script>
$(function hide_mouse_move() {
    $(document).mousemove(function() {
        moving();})
});
function pycmd(a){parent.pycmd(a)};
function moving(){parent.moving()};
</script>
`;

//executes in iFrame
$(document).ready(function(){
    $("#bottomiFrame").attr("srcdoc", url+mouseMove);
});

