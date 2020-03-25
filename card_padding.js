//No Distractions Full Screen v4.0
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
	var zF = window.devicePixelRatio/window.defaultScale
	var percent = (height/(window.innerHeight*zF))*100; //pads cards by height of answer button
	$(".NDFS").css("height", percent + '%');
};
