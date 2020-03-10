//var cursorIdleTimer = 5000; //Defined in python
$(function hide_cursor() {
    if (cursorIdleTimer >= 0){
        var cursorHidden = false;
        var timer = setTimeout(function () {
                //$('*').css({cursor: 'none'});
                pycmd("cursor_hide");
                console.log("cursor_hide");
                cursorHidden = true;
                }, cursorIdleTimer);
        $(document).mousemove(function () {
            clearTimeout(timer);
            timer = setTimeout(function () {
                //$('*').css({cursor: 'none'});
                pycmd("cursor_hide");
                console.log("cursor_hide");
                cursorHidden = true;
                }, cursorIdleTimer);
            if (cursorHidden) {
                //$('*').css({cursor: 'default'});
                pycmd("cursor_show");
                console.log("cursor_show");
                cursorHidden = false;
                return
            }
        });
    }
});