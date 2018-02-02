#!/usr/bin/env pwsh

# For the right Permission
# Set-ExecutionPolicy Bypass -Scope CurrentUser
$Documents = [Environment]::GetFolderPath('MyDocuments')

Write-Host "Installing blend_net dependecies:" -ForegroundColor Yellow
Write-Host "- Blender (networkx, pandas, matplotlib and numpy)"
. ".\shell_utils\pwsh\install_blender.ps1"

If( $args[1] -eq $null ) { $path2out = "toolchain" } # specify path to install programs
Else {  $path2out = $args[1] }
Write-Host "Installation path : $env:HOMEDRIVE$env:HOMEPATH\$path2out" -ForegroundColor Yellow


Push-Location
Set-Location $env:HOMEDRIVE$env:HOMEPATH
New-Item -Path $path2out -ItemType directory -Force > $null
New-Item -Path $Documents\WindowsPowerShell -ItemType directory -Force > $null
Set-Location $path2out


Write-Host "Looking for packages..."

# Blender download
If( -Not (Get-Command blender -ErrorAction SilentlyContinue) ){ # blender not installed
    Write-Host "blender not FOUND" -ForegroundColor Red
    If( $args[0] -eq "-y" -Or $args[0] -eq "-Y" -Or $args[0] -eq "yes" ){ install_blender "https://builder.blender.org/download/blender-2.79-78a77fe-win64.zip" "." $true networkx, pandas, matplotlib, numpy }
    Else{
        $CONFIRM = Read-Host -Prompt "Do you want install it? [y/n]"
        If($CONFIRM -eq "N" -Or $CONFIRM -eq "n"){ Write-Host "Abort" -ForegroundColor Red }
        Else{ install_blender "https://builder.blender.org/download/blender-2.79-78a77fe-win64.zip" "." $true networkx, pandas, matplotlib, numpy }
    }
}
Else{ Write-Host "blender FOUND" -ForegroundColor Green}

Pop-Location
