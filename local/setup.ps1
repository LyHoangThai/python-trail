[CmdletBinding()]
param([switch]$SkipInstall, [switch]$NoOpen)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

function Refresh-Tools {
    $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
    foreach ($candidate in @("$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin", "$env:ProgramFiles\Docker\Docker\resources\bin", "$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin")) {
        if (Test-Path -LiteralPath $candidate) { $env:Path += ';' + $candidate }
    }
}
function Install-PackageIfMissing([string]$Command,[string]$Id,[switch]$UserScope) {
    Refresh-Tools
    if (Get-Command $Command -ErrorAction SilentlyContinue) { return }
    if ($SkipInstall) { throw "$Command is missing. Run setup.ps1 without -SkipInstall to install prerequisites." }
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'Install Microsoft App Installer from the Microsoft Store (provides winget), then rerun setup.ps1.' }
    Write-Host "Installing $Id. This downloads software and accepts its package/source agreements. Windows may request permission."
    $installArgs = @('install','--id',$Id,'--exact','--source','winget','--accept-source-agreements','--accept-package-agreements')
    if ($UserScope) { $installArgs += @('--scope','user') }
    & winget @installArgs
    if ($LASTEXITCODE -notin @(0,3010,-1978335189)) { throw "Could not install $Id. Review the installer output, then rerun setup." }
    Refresh-Tools
}

Write-Host 'Python Trail local setup: Docker Desktop + VS Code + containerized Python, worker and database.'
Write-Host 'Internet is required for the first setup. Existing student files and database volumes are preserved.'
Refresh-Tools
$wslVersionText = (& wsl.exe --version 2>$null | Out-String) -replace "`0",''
if ($LASTEXITCODE -ne 0) {
    if ($SkipInstall) { throw 'A current WSL 2 is required. Run setup without -SkipInstall.' }
    Write-Host 'WSL needs installation or updating. Windows may show an administrator prompt.'
    $wslInstall = Start-Process -FilePath 'wsl.exe' -ArgumentList @('--install','--no-distribution') -Verb RunAs -WindowStyle Hidden -PassThru -Wait
    Write-Host 'WSL setup was attempted. Restart Windows if prompted, then rerun setup.ps1. Firmware virtualization must be enabled.'
    exit 1
}
if ($wslVersionText -match '(\d+\.\d+\.\d+)') {
    if ([version]$Matches[1] -lt [version]'2.1.5') {
        if ($SkipInstall) { throw 'Update WSL to 2.1.5 or later, then rerun setup.' }
        & wsl.exe --update
        if ($LASTEXITCODE -ne 0) { throw 'WSL update failed. Update WSL as administrator, then rerun setup.' }
        Write-Host 'WSL updated. Restart Windows if prompted, then rerun setup.ps1.'
        exit 1
    }
}
Install-PackageIfMissing 'docker' 'Docker.DockerDesktop'
Install-PackageIfMissing 'code' 'Microsoft.VisualStudioCode' -UserScope
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Docker installed. Restart Windows or open a new PowerShell window, then rerun setup.ps1.' }
& docker info *> $null
if ($LASTEXITCODE -ne 0) {
    $desktop = @("$env:LOCALAPPDATA\Programs\DockerDesktop\Docker Desktop.exe", "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe") | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if ($desktop) { Start-Process -FilePath $desktop -WindowStyle Hidden }
    Write-Host 'Waiting for Docker Desktop. On first launch, open Docker Desktop and finish its terms/setup screens. Use Linux containers.'
    $ready = $false
    for ($n=0; $n -lt 24; $n++) {
        & docker info *> $null
        if ($LASTEXITCODE -eq 0) { $ready=$true; break }
        Start-Sleep -Seconds 5
    }
    if (-not $ready) { throw 'Docker is not ready. Finish Docker Desktop setup or restart Windows, then rerun setup.ps1.' }
}
& docker compose version
if ($LASTEXITCODE -ne 0) { throw 'Docker Compose is missing. Update Docker Desktop and retry.' }
if (-not (Test-Path -LiteralPath '.env')) {
    $bytes = New-Object byte[] 32
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($bytes); $rng.Dispose()
    $password = [BitConverter]::ToString($bytes).Replace('-','').ToLowerInvariant()
    $studentPath = (Join-Path $PSScriptRoot 'student').Replace('\','/')
    [System.IO.File]::WriteAllText((Join-Path $PSScriptRoot '.env'), "TRAIL_DB_PASSWORD=$password`nHOST_STUDENT_DIR='$studentPath'`n", (New-Object System.Text.UTF8Encoding $false))
} else {
    # Moving the extracted folder should not rotate the password of an existing DB.
    $envPath = Join-Path $PSScriptRoot '.env'
    $lines = @(Get-Content -LiteralPath $envPath | Where-Object { $_ -notmatch '^HOST_STUDENT_DIR=' })
    $studentPath = (Join-Path $PSScriptRoot 'student').Replace('\','/')
    $lines += "HOST_STUDENT_DIR='$studentPath'"
    [System.IO.File]::WriteAllLines($envPath, $lines, (New-Object System.Text.UTF8Encoding $false))
}
& code --install-extension ms-vscode-remote.remote-containers
if ($LASTEXITCODE -ne 0) { throw 'Could not install the VS Code Dev Containers extension. Check your connection and rerun.' }
& docker compose up -d --build --wait
if ($LASTEXITCODE -ne 0) { throw 'Containers did not start. Run docker compose logs app worker db for details.' }
Write-Host 'Ready: http://localhost:8765'
Write-Host 'In VS Code: Ctrl+Shift+P -> Dev Containers: Reopen in Container.'
Write-Host 'Save a quest file; Ctrl+Shift+P -> Tasks: Run Test Task -> Trail: Check current quest.'
if (-not $NoOpen) {
    & code --new-window (Join-Path $PSScriptRoot 'student')
    Start-Process 'http://localhost:8765'
}
