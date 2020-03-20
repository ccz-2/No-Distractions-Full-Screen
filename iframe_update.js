//var url = '';
url = decodeURIComponent(url);

scripts = `<script>
function pycmd(a){parent.pycmd(a)};

var scale = ` + window.defaultScale + `;
function resize(){
    document.body.style.zoom = scale/window.devicePixelRatio;
}

function changeScale(x){ //called from parent
	scale = x;
	resize();
}

window.visualViewport.addEventListener('resize', resize);
window.addEventListener('DOMContentLoaded', resize);
</script>
`;

//executes in iFrame
$(document).ready(function(){
    $("#bottomiFrame").attr("srcdoc", url + scripts);
});