//var url = '';
url = decodeURIComponent(url);

scripts = `<script>
function pycmd(a){parent.pycmd(a)};
</script>
`;

//executes in iFrame
$(document).ready(function(){
    $("#bottomiFrame").attr("srcdoc", url + scripts);
});

