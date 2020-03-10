//No Distractions Full Screen v3.0
//var height = 100 //Defined in python

$('body').append(`
<div class="NDFS"></div>

<style>
  .NDFS {
    position: absolute;
    border-style: solid;
    border-color: transparent;
    //background: red;
  }
</style>
`);

function calcPadding(height){
	var percent = (height/window.innerHeight)*100; //pads cards by height of answer button
	$(".NDFS").css("height", percent + '%');
	//console.log('answerH: ' + height);
	//console.log('windowH: ' + window.innerHeight);
	//console.log('%: ' + percent);
};

/*
$("*").on({
    touchstart: function(){
    	console.log('touchstart')
    },
    touchend: function(){
    	console.log('touchend')
    },
    touchcancel: function(){
    	console.log('touchcancel')
    }
});*/