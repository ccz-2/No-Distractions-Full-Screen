//No Distractions Full Screen v4.0
//Called from resize events and mutation observer in parent
//var scale = 2; //called from python
function resize(){
    document.body.style.zoom = scale/window.devicePixelRatio;
}

function changeScale(x){ //called from parent
  scale = x;
  resize();
}

//Hack to remove wallpaper applied by Dancing Baloney addon
//$('body').append('<style>.before::before {content:none}</style>');
//$('body').addClass('before')

window.visualViewport.addEventListener('resize', resize);