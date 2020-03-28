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
scriptsDummy = `
<script>
	function pycmd(a){};
	function finishedLoad(){};
	parent.pycmd('NDFS-iFrameDummy-DOMReady')
</script>
`;

if (!$('#bottomiFrame').length){
	//bottomHover is parent for css hover to work
	//bottomiFrame is needed for draggable.js (need to be parent of cover)
	$('body').append(`
	<div id='bottomHover'>
    <div id='outer'>
      <div class="bottomWrapper noZoom">
        <iframe id='bottomiFrame' frameborder="0" scrolling="no">
        </iframe>
        <div id = 'cover'></div>
      </div>
        <iframe id='bottomiFrameBkgnd' class='noZoom' frameborder="0" scrolling="no">
        </iframe>
    </div>
  	</div>


	<style>
	#bottomHover {
      //background-color: red;
      //border: 1px solid black;
      position: fixed;
      width:100%;
      height: 2%;
      bottom: 0px;
      left: 0px;
      z-index: 1;
      pointer-events: none;
	}
	
	#outer{
	  //background-color: navy;
	  width: auto;
	  height: auto;
	  bottom: 0;
	  position: fixed;
	  pointer-events: none;
	  left: 50vw;
	  z-index: -10;
	}

	.bottomWrapper {
	  //border: 1px solid purple;
	  position: relative;
	  left: -50%;
	  border-radius: 5px;
	  margin: 0px;
	  padding: 0px;
	  pointer-events: auto;
	  touch-action: none;
	  user-select: none;
	  overflow: hidden;
	  width: auto;
	  height: auto;
	}
	
	#bottomiFrame {
	  //border: 1px solid orange;
	  margin: 0px;
	  padding: 0px;
	  overflow: hidden;
	  user-select: none;
	  z-index: 1;
	  position: relative;
	  display: block;
	  bottom: 0;
	  left: 0;
	}

	#cover{
      //background-color: hotpink;
      pointer-events: auto;
	  position: absolute;
	  top: 0;
	  height: 100%;
	  width: 100%;
	  z-index: 5;
	}

	#bottomiFrameBkgnd {
	  //background-color: yellow;
	  overflow: hidden;
	  display:block;
	  margin: 0px;
	  position: fixed;
	  bottom: 0;
	  left: 0;
	  width: 100%;
	  user-select: none;
	  touch-action: none;
	  pointer-events: none;
	  z-index: -10;
	}
	</style>
	`);
}
$("#cover").hide(); //cover only shown when dragging iframe
$("#bottomiFrame").attr("srcdoc", url + scripts);
$("#bottomiFrameBkgnd").attr("srcdoc", url + scriptsDummy); // no communication with python

function scriptExec(js) { 
	js = decodeURIComponent(js) //% encoded
	if (js.includes('<<<FOR BKGND>>>')){
		val = $('#bottomiFrameBkgnd')[0].contentWindow.eval(js);
	}
	else if (js.includes('<<<FOR ACTUAL>>>')){
		val = $('#bottomiFrame')[0].contentWindow.eval(js);
	}
	else {
		val = $('#bottomiFrame')[0].contentWindow.eval(js);
		$('#bottomiFrameBkgnd')[0].contentWindow.eval(js);
	}
	return val
}