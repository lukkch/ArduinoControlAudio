Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run "python ControlAudioDevice+Volume.py", 0
Set WshShell = Nothing