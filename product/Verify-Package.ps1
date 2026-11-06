$ErrorActionPreference='Stop'
$manifest=Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') | ConvertFrom-Json
foreach ($entry in $manifest.files) {
    $path=Join-Path $PSScriptRoot $entry.path
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing file: $($entry.path)" }
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256) { throw "Changed file: $($entry.path)" }
}
Write-Host "Verified $($manifest.files.Count) shipped files for $($manifest.product) $($manifest.version)."
Write-Host 'Run this before setup; assignment edits after using the sample are expected to change hashes.'
