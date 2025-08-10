!+q::      
    RunWait, %ComSpec% /c "E:\Files\Documents\Jared\Work\dev\batch\src\capture\runner.bat", , Hide
    FileRead, ItemNameText, E:\Files\Documents\Jared\Work\dev\batch\tmp\item_name.txt
    Clipboard = %ItemNameText%
    SplashTextOn 200,20,Hey I Captured item name as,%ItemNameText%
    SetTitleMatchMode, 2
    WinActivate, Inkscape
    Sleep 1500
    Send ^+!q
    SplashTextOff

Return
