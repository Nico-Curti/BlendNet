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

# Blender download
If( -Not (Get-Command blender -ErrorAction SilentlyContinue) ){ # blender not installed
    Write-Host "blender not FOUND" -ForegroundColor Red
    If( $args[0] -eq "-y" -Or $args[0] -eq "-Y" -Or $args[0] -eq "yes" ){
        Write-Host "download Blender from http://download.blender.org/source/blender-2.79.tar.gz"
        $Job = Start-BitsTransfer -Source "http://download.blender.org/source/blender-2.79.tar.gz" -Asynchronous
        while (($Job.JobState -eq "Transferring") -or ($Job.JobState -eq "Connecting")) `
        { sleep 5;} # Poll for status, sleep for 5 seconds, or perform an action.

        Switch($Job.JobState)
        {
            "Transferred" {Complete-BitsTransfer -BitsJob $Job}
            "Error" {$Job | Format-List } # List the errors.
            default {"Other action"} #  Perform corrective action.
        }

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
            Write-Host "download Blender from http://download.blender.org/source/blender-2.79.tar.gz"
            $Job = Start-BitsTransfer -Source "http://download.blender.org/source/blender-2.79.tar.gz" -Asynchronous
            while (($Job.JobState -eq "Transferring") -or ($Job.JobState -eq "Connecting")) `
            { sleep 5;} # Poll for status, sleep for 5 seconds, or perform an action.

            Switch($Job.JobState)
            {
                "Transferred" {Complete-BitsTransfer -BitsJob $Job}
                "Error" {$Job | Format-List } # List the errors.
                default {"Other action"} #  Perform corrective action.
            }
        }
}
Else{ Write-Host "blender FOUND" -ForegroundColor Green}




Pop-Location


