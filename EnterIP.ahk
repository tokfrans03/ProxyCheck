^I::
Loop
{
    FileReadLine, line, GoodIps.txt, %A_Index%
    if ErrorLevel
        break
    MsgBox, 4, , Line #%A_Index% is "%line%".  Continue?
    IfMsgBox, No
        return
    WinActivate, Inertia Version 3.1.3
    SendEvent {Click 1773, 59}
    SendEvent {Click 995, 420}
    Sleep, 100
    Send %line%
    SendEvent {Click 896, 530}
    Send {Esc}
    Send {Enter}
    ; return
}
MsgBox, The end of the file has been reached or there was a problem.
return