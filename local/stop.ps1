Set-Location -LiteralPath $PSScriptRoot
& docker compose stop
if ($LASTEXITCODE -ne 0) { throw 'Could not stop Python Trail. Check Docker Desktop.' }
Write-Host 'Stopped. Progress and code are preserved.'
