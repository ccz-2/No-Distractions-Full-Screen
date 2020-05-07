;global screentoggled:=false
;~F11::
    send #p
    Sleep, 1000
    Send {Home}{Down}
    ;if screentoggled
       send {Down}
    send {Enter}
    Sleep, 1000
    send {Esc}
    ;screentoggled := !screentoggled
;return