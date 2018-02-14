#!/usr/bin/env pwsh

$project = "Blender Graph Viewer"

# For the right Permission
# Set-ExecutionPolicy Bypass -Scope CurrentUser

$url_blender = "https://mirrors.dotsrc.org/blender/blender-release/Blender2.79/blender-2.79-windows64.zip"

$Documents = [Environment]::GetFolderPath('MyDocuments')

Write-Host "Installing $project dependecies:" -ForegroundColor Yellow
Write-Host "  - Blender (networkx, pandas, matplotlib and numpy)"
. ".\shell_utils\pwsh\install_blender.ps1"

If( $args[1] -eq $null ) { $path2out = "toolchain" } # specify path to install programs
Else {  $path2out = $args[1] }
Write-Host "Installation path : $env:HOMEDRIVE$env:HOMEPATH\$path2out" -ForegroundColor Green


Push-Location
Set-Location $env:HOMEDRIVE$env:HOMEPATH > $null
New-Item -Path $path2out -ItemType directory -Force > $null
New-Item -Path $Documents\WindowsPowerShell -ItemType directory -Force > $null
Set-Location $path2out

$log = "install_$project.log" 


Write-Host "Looking for packages..."

# Blender download
Write-Host "Blender identification: " -NoNewLine
If( -Not (Get-Command blender -ErrorAction SilentlyContinue) ){ # blender not installed
    Write-Host "FOUND" -ForegroundColor Red
    If( $args[0] -eq "-y" -Or $args[0] -eq "-Y" -Or $args[0] -eq "yes" ){
        Start-Transcript -Append -Path $log 
        install_blender $url_blender "." $true networkx, pandas, matplotlib, numpy 
        Stop-Transcript
    }
    Else{
        $CONFIRM = Read-Host -Prompt "Do you want install it? [y/n]"
        If($CONFIRM -eq "N" -Or $CONFIRM -eq "n"){ Write-Host "Abort" -ForegroundColor Red }
        Else{ 
            Start-Transcript -Append -Path $log
            install_blender $url_blender "." $true networkx, pandas, matplotlib, numpy 
            Stop-Transcript
        }
    }
}
Else{ Write-Host "FOUND" -ForegroundColor Green}

Pop-Location > $null
