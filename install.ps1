#!/usr/bin/env pwsh

# $args[0] = -y
# $args[1] = installation path from root
# $args[2] = silent mode (true/false)

$confirm = $args[0]
If( $args[1] -eq $null )
{
  $path2out = "toolchain"
} # specify path to install programs
Else
{
  $path2out = $args[1]
}
$silent = $args[2]

$PROFILE

$project = "Blender Graph Viewer"
$log = "install_$project.log"

# For the right Permission
# Set-ExecutionPolicy Bypass -Scope CurrentUser

$Documents = [Environment]::GetFolderPath('MyDocuments')


Write-Host "Installing $project dependecies:" -ForegroundColor Yellow
Write-Host "  - Blender (networkx, pandas, matplotlib and numpy)"
. ".\shut\pwsh\install_blender.ps1"

Write-Host "Installation path : $env:HOMEDRIVE$env:HOMEPATH\$path2out" -ForegroundColor Green

Push-Location
Set-Location $env:HOMEDRIVE$env:HOMEPATH > $null
New-Item -Path $path2out -ItemType directory -Force > $null
New-Item -Path $Documents\WindowsPowerShell -ItemType directory -Force > $null
Set-Location $path2out

Write-Host "Looking for packages..."

# Blender download
if ( $silent )
{
  Start-Transcript -Append -Path $log
}
install_blender -add2path $true -confirm $confirm -modules networkx, pandas, matplotlib, numpy
if ( $silent )
{
  Stop-Transcript
}

Pop-Location > $null
