# Create Ramgarh Escape Windows Shortcuts with custom game logo icon (.ico)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$rootDir = (Get-Item "$scriptDir\..").FullName
$iconPath = "$rootDir\icon.ico"
$batPath = "$rootDir\run_game.bat"
$desktopDir = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)

Write-Host "Creating game shortcuts with official Ramgarh Escape logo..." -ForegroundColor Yellow

$WshShell = New-Object -ComObject WScript.Shell

# 1. Project folder shortcut
$folderShortcut = "$rootDir\Ramgarh Escape.lnk"
$s1 = $WshShell.CreateShortcut($folderShortcut)
$s1.TargetPath = $batPath
$s1.WorkingDirectory = $rootDir
$s1.IconLocation = "$iconPath,0"
$s1.Description = "Play Ramgarh Escape - Retro Frontier Runner"
$s1.Save()
Write-Host "  [CREATED] Folder shortcut: $folderShortcut" -ForegroundColor Green

# 2. Desktop shortcut
$desktopShortcut = "$desktopDir\Ramgarh Escape.lnk"
$s2 = $WshShell.CreateShortcut($desktopShortcut)
$s2.TargetPath = $batPath
$s2.WorkingDirectory = $rootDir
$s2.IconLocation = "$iconPath,0"
$s2.Description = "Play Ramgarh Escape - Retro Frontier Runner"
$s2.Save()
Write-Host "  [CREATED] Desktop shortcut: $desktopShortcut" -ForegroundColor Green

# 3. Folder icon customization via desktop.ini
$iniPath = "$rootDir\desktop.ini"
$iniContent = @"
[.ShellClassInfo]
IconResource=$iconPath,0
[ViewState]
Mode=
Vid=
FolderType=Generic
"@
Set-Content -Path $iniPath -Value $iniContent -Force
attrib +h +s "$iniPath"
attrib +r "$rootDir"
Write-Host "  [CONFIGURED] Folder icon via desktop.ini" -ForegroundColor Green

Write-Host "Windows shortcuts and logo icons installed successfully!" -ForegroundColor Cyan
