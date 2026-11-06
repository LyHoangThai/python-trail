$ErrorActionPreference='Stop'
Write-Host 'This checks the real app, PostgreSQL, and worker. It records quest 1 as completed.'
$headers=@{'X-Trail-Client'='vscode'}
$body=@{quest=1;source='print("Hello, explorer!")'} | ConvertTo-Json
$job=Invoke-RestMethod -Method Post -Uri 'http://localhost:8765/api/submit' -ContentType 'application/json' -Headers $headers -Body $body
$result=$null
for ($i=0;$i -lt 60;$i++) {
    $result=Invoke-RestMethod -Uri "http://localhost:8765/api/jobs/$($job.id)"
    if ($result.status -eq 'done') { break }
    Start-Sleep -Seconds 1
}
if (-not $result.passed) { throw "Worker check failed or timed out: $($result.feedback)" }
$progress=Invoke-RestMethod -Uri 'http://localhost:8765/api/progress'
if (1 -notin @($progress.completed | ForEach-Object { $_.quest })) { throw 'The worker passed, but completion was not found in the database.' }
Write-Host 'PASS: submission -> worker -> stored completion -> parent dashboard API.'
