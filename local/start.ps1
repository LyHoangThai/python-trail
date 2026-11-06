[CmdletBinding()]
param([switch]$WithVSCode)
$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$composeArgs=@('compose')
if ($WithVSCode) { $composeArgs+=@('--profile','vscode') }
$composeArgs+=@('up','-d','--wait')
& docker @composeArgs
if ($LASTEXITCODE -ne 0) { throw 'Start Docker Desktop, then rerun start.ps1.' }
Start-Process 'http://localhost:8765/learn'
if ($WithVSCode) { & code (Join-Path $PSScriptRoot 'student') }
