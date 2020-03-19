//var url = '';
defaultZoom = 2;
url = decodeURIComponent(url);

scripts = `<script>
function pycmd(a){parent.pycmd(a)};

function resize (){
    document.body.style.zoom = ` + defaultZoom + `/window.devicePixelRatio;
}
window.visualViewport.addEventListener('resize', resize);

</script>
`;

//executes in iFrame
$(document).ready(function(){
    $("#bottomiFrame").attr("srcdoc", url + scripts);
});

