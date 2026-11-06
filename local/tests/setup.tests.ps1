$ErrorActionPreference='Stop'
$scriptPath=Join-Path (Split-Path $PSScriptRoot -Parent) 'setup.ps1'
$tokens=$null; $parseErrors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseFile($scriptPath,[ref]$tokens,[ref]$parseErrors)
if ($parseErrors.Count) { throw ($parseErrors | Out-String) }
$probe=$ast.Find({param($node) $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq 'Get-DockerServerType'},$true)
if (-not $probe) { throw 'Docker readiness probe is missing.' }
# Import only the probe, never the installer itself.
Invoke-Expression $probe.Extent.Text
$wslCommands=$ast.FindAll({param($node) $node -is [System.Management.Automation.Language.CommandAst] -and $node.GetCommandName() -match '^wsl(\.exe)?$'},$true)
if ($wslCommands.Count) { throw 'Setup must not invoke WSL.' }

function docker { $global:LASTEXITCODE=0; 'linux' }
if ((Get-DockerServerType) -ne 'linux') { throw 'Linux engine was not detected.' }
function docker { $global:LASTEXITCODE=0; 'windows' }
if ((Get-DockerServerType) -ne 'windows') { throw 'Windows engine was not detected.' }
function docker { & $env:ComSpec /d /c 'echo Engine unavailable 1>&2 & exit /b 1' }
if ($null -ne (Get-DockerServerType)) { throw 'Unavailable engine must return null.' }
if ($ErrorActionPreference -ne 'Stop') { throw 'Error preference was not restored.' }
Write-Host 'PASS: setup syntax, no WSL commands, Linux/Windows engine detection, native stderr failure handling.'
