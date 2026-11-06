[CmdletBinding()]
param([switch]$WithVSCode)
$ErrorActionPreference='Stop'
& (Join-Path $PSScriptRoot 'local\start.ps1') -WithVSCode:$WithVSCode
