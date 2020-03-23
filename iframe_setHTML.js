//No Distractions Full Screen v4.0
//var url = '';
var op = 0.5;
url = decodeURIComponent(url);
scripts = `
<script>
	function pycmd(a){parent.pycmd(a)};
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
	    //background-color: red;
	}
	
	#outer{
	  bottom: 0;
	  position: fixed;
	  left: 50%;
	  //background-color: green;
	}
	
	.bottomWrapper {
	  position: relative;
	  left: -50%;
	  //background-color: red;
	  border-radius: 5px;
	  margin: 0px;
	  pointer-events: auto;
	  //touch-action: none;
	  opacity: ` + op + `
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
	
	.fade-in {
	  animation-name: fadeInOpacity;
	  animation-iteration-count: 1;
	  animation-timing-function: ease-in-out;
	  animation-duration: 0.15s;
	}
	
	@keyframes fadeInOpacity {
	  0% {
	    opacity: ` + op + `;
	  }
	  100% {
	    opacity: 1;
	  }
	}
	
	</style>
	`);
}
$("#bottomiFrame").attr("srcdoc", url + scripts);

var stopped = true;
function scriptExec() {
	if (stopped){
		stopped = false;
		var waitForJQuery = setInterval(function () {
		    if ($('#bottomiFrame')[0].contentWindow.eval("typeof $ != 'undefined'")) {
				while (scriptQueue.length != 0){
					js = scriptQueue.shift()
					$('#bottomiFrame')[0].contentWindow.eval("$(document).ready(function(){"+js+"});");
				}
        		clearInterval(waitForJQuery);
        		stopped = true;
		    }
		}, 10);
	}
}

//executes in iFrame
/*
$(document).ready(function(){
	var checkExist = setInterval(function() {
	   if ($('#bottomiFrame').length) {
    		$("#bottomiFrame").attr("srcdoc", url + scripts);
	     	clearInterval(checkExist);
	   }
	}, 50);
});*/