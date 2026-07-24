
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\Islam Talicom\Desktop\EduManage Academy.lnk")
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = "`"F:\M_100184\EduManage_Launcher.vbs`""
$Shortcut.WorkingDirectory = "F:\M_100184"
$Shortcut.Description = "EduManage Academy - গাজীমাহমুদ নিম্ন মাধ্যমিক বিদ্যালয়"
if (Test-Path "F:\M_100184\static\logo.png") {
    $Shortcut.IconLocation = "F:\M_100184\static\logo.png"
}
$Shortcut.Save()
