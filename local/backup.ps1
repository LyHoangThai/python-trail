$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$backupDir = Join-Path $PSScriptRoot 'backups'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$stamp=Get-Date -Format 'yyyyMMdd-HHmmss'
$dumpPath=Join-Path $backupDir "progress-$stamp.dump"
& docker compose exec -T db pg_dump --username=trail --dbname=trail --format=custom --file=/tmp/trail-backup.dump
if ($LASTEXITCODE -ne 0) { throw 'Database backup failed. Check that the containers are running.' }
& docker compose cp db:/tmp/trail-backup.dump $dumpPath
if ($LASTEXITCODE -ne 0) { throw 'Could not copy the database backup.' }
Compress-Archive -LiteralPath (Join-Path $PSScriptRoot 'student') -DestinationPath (Join-Path $backupDir "student-$stamp.zip")
Write-Host "Saved database and student code in $backupDir. Keep the .env file with this installation; do not share it."
