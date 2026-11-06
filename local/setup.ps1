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

function Get-DockerServerType {
    # Windows PowerShell 5.1 turns native stderr into NativeCommandError with
    # ErrorActionPreference=Stop. An unavailable engine is an expected probe result.
    $savedPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $serverType = (& docker info --format '{{.OSType}}' 2>$null | Out-String).Trim()
        $probeExit = $LASTEXITCODE
    } finally { $ErrorActionPreference = $savedPreference }
    if ($probeExit -eq 0 -and $serverType -in @('linux','windows')) { return $serverType }
    return $null
}

Write-Host 'Python Trail local setup: Docker Desktop + VS Code + containerized Python, worker and database.'
Write-Host 'Internet is required for the first setup. Existing student files and database volumes are preserved.'
Refresh-Tools
Install-PackageIfMissing 'docker' 'Docker.DockerDesktop'
Install-PackageIfMissing 'code' 'Microsoft.VisualStudioCode' -UserScope
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Docker installed. Restart Windows or open a new PowerShell window, then rerun setup.ps1.' }
$engine = Get-DockerServerType
if (-not $engine) {
    $desktop = @("$env:LOCALAPPDATA\Programs\DockerDesktop\Docker Desktop.exe", "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe") | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if ($desktop) { Start-Process -FilePath $desktop -WindowStyle Hidden }
    Write-Host 'Waiting for Docker Desktop. Open Docker Desktop and finish its first-launch setup. Select Linux containers.'
    for ($n=0; $n -lt 24; $n++) {
        $engine = Get-DockerServerType
        if ($engine) { break }
        Start-Sleep -Seconds 5
    }
    if (-not $engine) { throw 'Docker Desktop is not ready. Open it, finish its backend/setup prompts, then rerun setup.ps1. This script does not install or configure WSL.' }
}
if ($engine -ne 'linux') { throw 'Docker Desktop is using Windows containers. Switch to Linux containers in Docker Desktop, then rerun setup.ps1.' }
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
