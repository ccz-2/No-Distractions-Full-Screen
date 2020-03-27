//Called from resize events and mutation observer in parent
//var scale = 2; //called from python
function resize(){
    document.body.style.zoom = scale/window.devicePixelRatio;
}

function changeScale(x){ //called from parent
  scale = x;
  resize();
}

function getHeight() {
  if ($('table:not([id="innertable"])')[0] != null){
  	height = $('table:not([id="innertable"])').height();
  }
  else {
  	height = document.body.getBoundingClientRect().height;
  }
  return height
}

window.visualViewport.addEventListener('resize', resize);