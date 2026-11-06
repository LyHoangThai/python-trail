$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
& docker compose up -d --wait
if ($LASTEXITCODE -ne 0) { throw 'Start Docker Desktop, then rerun start.ps1.' }
Start-Process 'http://localhost:8765'
& code (Join-Path $PSScriptRoot 'student')
