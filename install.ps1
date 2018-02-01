#!/usr/bin/env pwsh

# For the right Permission
# Set-ExecutionPolicy Bypass -Scope CurrentUser
$Documents = [Environment]::GetFolderPath('MyDocuments')

Write-Host "Installing blend_net dependecies:" -ForegroundColor Yellow
Write-Host "- Blender (networkx and pandas)"

If( $args[1] -eq $null ) { $path2out = "toolchain" } # specify path to install programs
Else {  $path2out = $args[1] }
Write-Host "Installation path : $env:HOMEDRIVE$env:HOMEPATH\$path2out" -ForegroundColor Yellow


Push-Location
Set-Location $env:HOMEDRIVE$env:HOMEPATH
New-Item -Path $path2out -ItemType directory -Force > $null
New-Item -Path $Documents\WindowsPowerShell -ItemType directory -Force > $null
Set-Location $path2out


Write-Host "Looking for packages..."

function Expand-Tar($tarFile, $dest) {
    if (-not (Get-Command Expand-7Zip -ErrorAction Ignore)) {
        Install-Package -Scope CurrentUser -Force 7Zip4PowerShell > $null
    }
    Expand-7Zip $tarFile $dest
}

# Blender download
If( -Not (Get-Command blender -ErrorAction SilentlyContinue) ){ # blender not installed
    Write-Host "blender not FOUND" -ForegroundColor Red
    If( $args[0] -eq "-y" -Or $args[0] -eq "-Y" -Or $args[0] -eq "yes" ){
        Write-Host "cloning Blender from git://git.blender.org/blender.git"
        git clone git://git.blender.org/blender.git
        cd blender
        git submodule update --init --recursive
        git submodule foreach git checkout master
        git submodule foreach git pull --rebase origin master

        svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/win64_vc14  lib/win64_vc14
        make full
        
    # pip installer
        $Job = Start-BitsTransfer -Source "https://bootstrap.pypa.io/get-pip.py" -Asynchronous
        while (($Job.JobState -eq "Transferring") -or ($Job.JobState -eq "Connecting")) `
        { sleep 5;} # Poll for status, sleep for 5 seconds, or perform an action.

        Switch($Job.JobState)
        {
            "Transferred" {Complete-BitsTransfer -BitsJob $Job}
            "Error" {$Job | Format-List } # List the errors.
            default {"Other action"} #  Perform corrective action.
        }


    }
    Else{
        $CONFIRM = Read-Host -Prompt "Do you want install it? [y/n]"
        If($CONFIRM -eq "N" -Or $CONFIRM -eq "n"){ Write-Host "Abort" -ForegroundColor Red }
        Else{
            Write-Host "cloning Blender from https://github.com/maiself/blender"
            git clone https://github.com/maiself/blender
        }
}
Else{ Write-Host "blender FOUND" -ForegroundColor Green}




Pop-Location


