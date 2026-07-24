Set WshShell = CreateObject("WScript.Shell")
strPath = WshShell.CurrentDirectory
WshShell.Run "pythonw.exe """ & strPath & "\launch_desktop.pyw""", 0, False
