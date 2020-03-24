//No Distractions Full Screen v4.0
//var url = '';
url = decodeURIComponent(url);
scripts = `
<script>
	function pycmd(a){parent.pycmd(a)};
	function finishedLoad(){parent.finishedLoad()};
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

//getHeight%28%29%3B
var scriptQueue = [];

function queueJS(js){
	queueJS_cb(js, function(results) {
		console.log(results)
		return results
	})
}

function queueJS_cb(js, callback) {
	js = decodeURIComponent(js) //% encoded
	scriptQueue.push(js);
	queueExec();
	var waitForReturn = setInterval(function () {
		var i = ret.findIndex(function(element){
			if(element[0] == js) {
				return element
			}
		});
		if (i>=0) {
			var val = ret[i][1];
			ret.splice(i,1);
			clearInterval(waitForReturn);
			callback(val);
		}
	}, 10);
}

var stopped = true;
var ret = [];
function queueExec() {
	//if (stopped){
		stopped = false;
		var waitForJQuery = setInterval(function () {
		    if ($('#bottomiFrame')[0].contentWindow.eval("typeof $ != 'undefined'")) {
				//while (scriptQueue.length != 0){
				var waitforiFrame = setInterval(function() {
					if ($('#bottomiFrame')[0].contentWindow.eval("document.readyState == 'complete'")){
						js = scriptQueue.shift()
						val = $('#bottomiFrame')[0].contentWindow.eval(js);
						ret.push([js,val])
						//Faster, but do not allow scripts to be callable after run
						//val = $('#bottomiFrame')[0].contentWindow.Function("return($(document).ready(function(){"+js+"}))")()
						//val = $('#bottomiFrame')[0].contentWindow.eval("$(document).ready(function(){"+js+"});");
					}
					else {
						console.log('failed to load script...retrying')
					}
					if (scriptQueue.length == 0){
						clearInterval(waitforiFrame)
						stopped = true;
					}
				}, 1);		
        		clearInterval(waitForJQuery);
		    }
		}, 10);
	//}
}

function scriptExec(js) { 
	js = decodeURIComponent(js) //% encoded
	var val = 'hi';
	var waitForJQuery = setInterval(function () {
	    if ($('#bottomiFrame')[0].contentWindow.eval("typeof $ != 'undefined'")) {
			var waitforiFrame = setInterval(function() {
				if ($('#bottomiFrame')[0].contentWindow.eval("document.readyState == 'complete'")){
					val = $('#bottomiFrame')[0].contentWindow.eval(js);
   					clearInterval(waitForJQuery);
   					clearInterval(waitforiFrame);
   					console.log('val: ' + val)
   					console.log(val)
					return val;
				}
				else {
					console.log('failed to load script...retrying')
				}
			}, 1);
	    }
	}, 10);

}

function callBack(js) { 
	js = decodeURIComponent(js) //% encoded
	val = $('#bottomiFrame')[0].contentWindow.eval(js);
	return val
}