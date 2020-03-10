//No Distractions Full Screen v3.0
//Uses interact.js
//var posX = 50;
//var posY = 50;

var target;

function getTarget(){
	target = document.querySelector('table:not([id="innertable"])');
}

//moves target to within window boundaries
function fitInWindow() {
  getTarget()
  if (target !== null){
  	var rect = target.getBoundingClientRect();
  	var x = parseFloat(target.getAttribute('data-x'));
  	var y = parseFloat(target.getAttribute('data-y'));
  	if (rect.x < 0){
  		updatePos(x - rect.x, y)
  	}
  	if (rect.right > window.innerWidth){
  		dx = rect.right - window.innerWidth
  		updatePos(x - dx , y)
  	}
  	if (rect.top < 0){
  		updatePos(x, y - rect.top )
  	}
  	if (rect.bottom > window.innerHeight){
  		dy = rect.bottom - window.innerHeight
  		updatePos(x, y - dy )
  	}
  }
}

$( window ).resize(function() {
  fitInWindow();
});

function updatePos(x, y){
	getTarget()
	target.style.transform = 'translate(' + x + 'px, ' + y + 'px)';
	target.setAttribute("data-x", x);
	target.setAttribute("data-y", y);
}

function enable_drag(){
// target elements with the "draggable" class
	getTarget()
	fitInWindow()
	if (!interact.isSet(target)){
		interact(target)
		  .draggable({
		    inertia: true,
		    enabled: true,
		    modifiers: [
		      	interact.modifiers.restrictRect({
		      	  restriction: '#canvas',
		      	  endOnly: true
		      	}),
      		  	interact.modifiers.snap({
      		    	targets: [
    					function () { //recursively calculates target original position (before transform)
							var el = target, offsetLeft = 0, offsetTop  = 0;
							do{
							    offsetLeft += el.offsetLeft;
							    offsetTop  += el.offsetTop;
							    el = el.offsetParent;
							} while( el );
    					  return {
    					    x: offsetLeft, //snap targets
    					    y: offsetTop,
    					    range: 30,
    					  }
    					}
      		    	],
		        	relativePoints: [
     				  { x: 0, y: 0} //snap to top-left
     				]
      		  	})
		    ],
		    autoScroll: false,
		    onmove: dragMoveListener,
		    onend: function (event) {
		    	var x = event.target.getAttribute('data-x');
				  var y = event.target.getAttribute('data-y');
		    	pycmd("draggable_pos: " + x + ", " + y);
		    }
		  })
	}
	else {
  		interact(target).draggable({enabled: true})
	}
  	$(target).css('-webkit-box-shadow', '0 0 10px LightBlue');
}

function dragMoveListener (event) {
  var target = event.target
  // keep the dragged position in the data-x/data-y attributes
  var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx
  var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy
  // translate the element
  target.style.transform = 'translate(' + x + 'px, ' + y + 'px)'
  target.setAttribute('data-x', x)
  target.setAttribute('data-y', y)
  //console.log(x +', '+ y)
}

function disable_drag(){
  getTarget();
  fitInWindow();
  interact(target).unset();
  //interact(target).draggable({enabled: false}); //Will occasionally stop working if disabled - better to unset
  $(target).css('-webkit-box-shadow', '');
}

var mousedown = false;
function activateHover(){
	getTarget();
	$(target).on({
	    mouseenter: function(){
	      //console.log('hover_in')
	      pycmd('hover_in');
	      fade_in(target);
	    },
	    mouseleave: function(){
	      //console.log('hover_out')
	      pycmd('hover_out');
	      fade_out(target)
	    },
    	touchstart: function(){
    	  //console.log('touchstart')
    	  pycmd('touchstart');
	      fade_in(target);
    	},
    	touchend: function(){
    	  //console.log('touchend')
    	  //pycmd('touchend');
	      fade_out(target)
        setTimeout(function(){pycmd('hover_out');}, 50); //undos automatic mouseenter at end of touchend
    	}
	});
  $('#canvas').on({
      mousedown: function(){
        mousedown = true;
      },
      mouseup: function(){
        mousedown = false;
      }
  });
}

function enable_bottomHover(){
  	getTarget();
	$( "#bottomHover" ).hover(
	  function() {
	    fade_in(target);
	  }, function() {
	    fade_out(target)
	  }
	);
}

function fade_in(target){
  $(target).css('animation-direction','normal');
  $(target).addClass('fade-in');
  $(target).css('opacity','1');  
  $(target).on("animationend", function(){
    $(this).removeClass('fade-in');
    });
}

function fade_out(target){
  if (!mousedown) { //prevents fanding out when dragging
    $(target).css('animation-direction','reverse');
    $(target).addClass('fade-in');
    $(target).css('opacity','');  
    $(target).on("animationend", function(){
      $(this).removeClass('fade-in');
      });
  }
}