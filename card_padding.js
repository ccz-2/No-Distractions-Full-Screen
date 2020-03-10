//No Distractions Full Screen v2.3
//var height = 100 //Defined in python
percent = (height/window.innerHeight)*100; //pads cards by height of answer button
//console.log('answerH: ' + height);
//console.log('windowH: ' + window.innerHeight);
//console.log('%: ' + percent);
$('body').append(`
<div class="NDFS"></div>

<style>
  .NDFS {
    height: ` + percent + `%;
    position: absolute;
    border-style: solid;
    border-color: transparent;
  }
</style>
`);