//No Distractions Full Screen v4.0
//var js = '';



js = decodeURIComponent(js);
if (typeof scriptQueue === 'undefined'){
	var scriptQueue = [];
}
scriptQueue.push(js);
scriptExec();
console.log(js);
console.log(scriptQueue.length)
//$('#bottomiFrame')[0].contentWindow.eval(`window.onload = function() {
//	`+js+`
//};`);

//$('#bottomiFrame').on('load', function(){
//	if ($('#bottomiFrame')[0].contentWindow.eval("typeof $ != 'undefined'")){
//    	console.log('hasdf')
//    	$('#bottomiFrame')[0].contentWindow.eval(js)
//    }
//});

//('#bottomiFrame')[0].contentWindow.eval(`document.addEventListener('DOMContentLoaded', function() {console.log('hi')});`);

//var waitForJQuery = setInterval(function () {
//    if ($('#bottomiFrame')[0].contentWindow.eval("typeof $ != 'undefined'")) {
//			$('#bottomiFrame')[0].contentWindow.eval(js)
//			clearInterval(waitForJQuery);
//		}
//	else {
//		console.log('not loaded')
//		}
//}, 1);




//var waitForJQuery = setInterval(function () {
//    if ($('#bottomiFrame')[0].contentWindow.eval("typeof $ != 'undefined'")) {
//		$('#bottomiFrame')[0].contentWindow.eval(js)
//        clearInterval(waitForJQuery);
//    }
//}, 1);

/*
//executes in iFrame
$(document).ready(function(){
	var checkExist = setInterval(function() {
		if ($('#bottomiFrame').length) {
			//console.log(js)
			$('#bottomiFrame')[0].contentWindow.eval(js);
			//$('#bottomiFrame').contents().find('body').append('<script>'+js+'</script>');
	     	clearInterval(checkExist);
		}
	//   $('#bottomiFrame').contents().find('body').append('<script>'+js+'</script>');
	//   clearInterval(checkExist);
	}, 100);

});
*/