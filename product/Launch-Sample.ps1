[CmdletBinding()]
param([switch]$SkipInstall,[switch]$NoOpen,[switch]$WithVSCode)
$ErrorActionPreference='Stop'
& (Join-Path $PSScriptRoot 'local\setup.ps1') -SkipInstall:$SkipInstall -NoOpen:$NoOpen -WithVSCode:$WithVSCode
