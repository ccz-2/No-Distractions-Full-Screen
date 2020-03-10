/* Defined in python: var cursorIdleTimer = ~;*/
$(function hide_cursor() {
    if (cursorIdleTimer >= 0){
    var timer;
    var fadeInBuffer = false;

    $(document).mousemove(function () {
        if (!fadeInBuffer) {
            if (timer) {
                console.log("clearTimer");
                clearTimeout(timer);
                timer = 0;
            }

                console.log("fadeIn");
            $('*').css({
                cursor: ''
            });
        } else {
             $('*').css({
                cursor: 'default'
            });
            fadeInBuffer = false;
        }


        timer = setTimeout(function () {
            console.log("fadeout");
             $('*').css({
                cursor: 'none'
            });
         
            fadeInBuffer = true;
        }, cursorIdleTimer)
    });
    $('*').css({
                cursor: 'none'
            });
    }
});