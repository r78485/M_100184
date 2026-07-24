import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
desktop_folder = os.path.join(os.path.expanduser("~"), "Desktop")
shortcut_path = os.path.join(desktop_folder, "EduManage Academy.lnk")
target_vbs = os.path.join(BASE_DIR, "EduManage_Launcher.vbs")
icon_path = os.path.join(BASE_DIR, "static", "logo.png")

# Windows PowerShell script to create shortcut with icon
ps_script = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = "`"{target_vbs}`""
$Shortcut.WorkingDirectory = "{BASE_DIR}"
$Shortcut.Description = "EduManage Academy - গাজীমাহমুদ নিম্ন মাধ্যমিক বিদ্যালয়"
if (Test-Path "{icon_path}") {{
    $Shortcut.IconLocation = "{icon_path}"
}}
$Shortcut.Save()
'''

ps_file = os.path.join(BASE_DIR, "make_shortcut.ps1")
with open(ps_file, "w", encoding="utf-8") as f:
    f.write(ps_script)

print(f"Shortcut script created at {ps_file}")
