//No Distractions Full Screen v4.0
//var url = '';
url = decodeURIComponent(url);
scripts = `
<script>
	function pycmd(a){parent.pycmd(a)};
	function finishedLoad(){parent.finishedLoad()};
	pycmd('NDFS-iFrame-DOMReady');
</script>
`;

if (!$('#bottomiFrame').length){
	$('body').append(`
	  <div id='outer'>
	    <div class="bottomWrapper">
	      <iframe id='bottomiFrame' frameborder="0" scrolling="no"">
	      </iframe>
	    </div>
	  </div>
	
	<div id='bottomHover'></div>
	
	<style>
	#bottomHover {
	    position: fixed;
	    width:100%;
	    height: 15px;
	    bottom: 0px;
	    left: 0px;
	    z-index: -999;
	}
	
	#outer{
	  bottom: 0;
	  position: fixed;
	  left: 50%;
	}
	
	.bottomWrapper {
	  position: relative;
	  left: -50%;
	  border-radius: 5px;
	  margin: 0px;
	  pointer-events: auto;
	  touch-action: none;
	  user-select: none;
	}
	
	#canvas{
	  position: fixed;
	  top: 0;
	  left: 0;
	  height: 100%;
	  width: 100%;
	  margin: 0px;
	  pointer-events: none;
	  background-color: teal;
	}
	
	#bottomiFrame {
	  display:block;
	  margin: 0px;
	  position: absolute;
	  bottom: 0;
	  user-select: none;
	}
	
	</style>
	`);
}
$("#bottomiFrame").attr("srcdoc", url + scripts);

function scriptExec(js) { 
	js = decodeURIComponent(js) //% encoded
	val = $('#bottomiFrame')[0].contentWindow.eval(js);
	return val
}