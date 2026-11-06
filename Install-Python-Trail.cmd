@echo off
setlocal
set "PYTHON_TRAIL_INSTALLER=%~f0"
start "" powershell.exe -NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden -Command "$lines=[IO.File]::ReadAllLines($env:PYTHON_TRAIL_INSTALLER); $i=[Array]::IndexOf($lines,'#--POWERSHELL--'); if($i -lt 0){throw 'Installer is incomplete'}; & ([scriptblock]::Create(($lines[($i+1)..($lines.Length-1)] -join [Environment]::NewLine)))"
exit /b
#--POWERSHELL--
[CmdletBinding()]
param([string]$InstallRoot=(Join-Path $env:LOCALAPPDATA 'PythonTrail'),[switch]$PrepareOnly)
$ErrorActionPreference='Stop'
[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12
$headers=@{'User-Agent'='PythonTrail-Installer';'Accept'='application/vnd.github+json'}
$root=[IO.Path]::GetFullPath($InstallRoot)
$rootPrefix=$root.TrimEnd('\')+'\'
function Assert-Child([string]$path){if(-not [IO.Path]::GetFullPath($path).StartsWith($rootPrefix,[StringComparison]::OrdinalIgnoreCase)){throw 'Installer path escaped its installation folder.'}}
$window=$null
if(-not $PrepareOnly){
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    [Windows.Forms.Application]::EnableVisualStyles()
    $window=New-Object Windows.Forms.Form
    $window.Text='Python Trail - Downloading setup'
    $window.ClientSize=New-Object Drawing.Size(540,185)
    $window.StartPosition='CenterScreen';$window.ControlBox=$false
    $window.BackColor=[Drawing.Color]::FromArgb(246,248,241)
    $heading=New-Object Windows.Forms.Label
    $heading.Text='Getting your learning lab ready...'
    $heading.Font=New-Object Drawing.Font('Segoe UI',16,[Drawing.FontStyle]::Bold)
    $heading.SetBounds(22,20,500,40)
    $status=New-Object Windows.Forms.Label
    $status.Font=New-Object Drawing.Font('Segoe UI',10)
    $status.SetBounds(24,77,490,70)
    $window.Controls.AddRange(@($heading,$status));$window.Show()
}
function Status([string]$text){if($window){$status.Text=$text;$window.Refresh();[Windows.Forms.Application]::DoEvents()}else{Write-Output $text}}
$scratch=$null
try {
    [void][IO.Directory]::CreateDirectory($root)
    Status 'Checking the release on GitHub. Internet is required.'
    $commit=Invoke-RestMethod -Uri 'https://api.github.com/repos/LyHoangThai/python-trail/commits/main' -Headers $headers -TimeoutSec 45
    $sha=[string]$commit.sha
    if($sha -notmatch '\A[0-9a-f]{40}\z'){throw 'GitHub returned an invalid release identity.'}
    $base='https://raw.githubusercontent.com/LyHoangThai/python-trail/'+$sha
    $channel=(Invoke-WebRequest -UseBasicParsing -Uri ($base+'/distribution/channel.json') -Headers $headers -TimeoutSec 45).Content | ConvertFrom-Json
    $version=[string]$channel.version;$checksum=[string]$channel.sha256
    if($version -notmatch '\A\d+\.\d+\.\d+\z' -or $checksum -notmatch '\A[0-9a-f]{64}\z'){throw 'The release information is invalid.'}
    $name='python-trail-sample-'+$version
    $destination=Join-Path $root $name;Assert-Child $destination
    $marker=Join-Path $destination '.package-sha256'
    if(Test-Path -LiteralPath $destination){
        if(-not (Test-Path -LiteralPath $marker) -or (Get-Content -Raw -LiteralPath $marker).Trim() -ne $checksum){throw 'This version folder already exists but was not installed by this launcher. Keep it intact and choose another installation folder.'}
        Status 'This version is already installed. Preparing to start it.'
    }else{
        $scratch=Join-Path $root ('download-'+[Guid]::NewGuid().ToString('N'));Assert-Child $scratch
        [void][IO.Directory]::CreateDirectory($scratch)
        $archive=Join-Path $scratch 'product.zip'
        Status ('Downloading Python Trail '+$version+' from GitHub...')
        $client=New-Object Net.WebClient
        try{
            $client.Headers['User-Agent']='PythonTrail-Installer'
            $task=$client.DownloadFileTaskAsync([Uri]($base+'/releases/'+$name+'.zip'),$archive)
            while(-not $task.IsCompleted){if($window){[Windows.Forms.Application]::DoEvents()};Start-Sleep -Milliseconds 100}
            $task.GetAwaiter().GetResult()
        }finally{$client.Dispose()}
        if((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $checksum){throw 'The download checksum did not match. No application code was started. Please retry.'}
        Status 'Verifying and unpacking your learning lab...'
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $zip=[IO.Compression.ZipFile]::OpenRead($archive)
        try{foreach($entry in $zip.Entries){$target=[IO.Path]::GetFullPath((Join-Path $scratch $entry.FullName));if(-not $target.StartsWith($scratch.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'The archive contains an unsafe path.'}}}finally{$zip.Dispose()}
        Expand-Archive -LiteralPath $archive -DestinationPath $scratch
        $payload=Join-Path $scratch $name;Assert-Child $payload
        if(-not(Test-Path -LiteralPath (Join-Path $payload 'Setup-App.ps1'))){throw 'The package is missing its setup application.'}
        $manifest=Get-Content -Raw -LiteralPath (Join-Path $payload 'manifest.json') | ConvertFrom-Json
        foreach($entry in $manifest.files){
            $file=[IO.Path]::GetFullPath((Join-Path $payload $entry.path))
            if(-not $file.StartsWith($payload.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'The manifest contains an unsafe path.'}
            if((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256){throw ('Package verification failed: '+$entry.path)}
        }
        # Preserve this managed installation's credentials and editable student files on updates.
        $currentFile=Join-Path $root 'current-version.txt'
        if(Test-Path -LiteralPath $currentFile){
            $previous=(Get-Content -Raw -LiteralPath $currentFile).Trim()
            if($previous -match '\A\d+\.\d+\.\d+\z'){
                $old=Join-Path $root ('python-trail-sample-'+$previous);Assert-Child $old
                $oldEnv=Join-Path $old 'local\.env'
                if(Test-Path -LiteralPath $oldEnv){Copy-Item -LiteralPath $oldEnv -Destination (Join-Path $payload 'local\.env')}
                $lessons=Get-Content -Raw -LiteralPath (Join-Path $payload 'local\app\lessons.json') | ConvertFrom-Json
                $assignments=@('playground.py')+@($lessons | ForEach-Object {$_.assignment_path})
                foreach($assignment in $assignments){
                    $source=Join-Path (Join-Path $old 'local\student') $assignment
                    $target=Join-Path (Join-Path $payload 'local\student') $assignment
                    Assert-Child $source;Assert-Child $target
                    if(Test-Path -LiteralPath $source){Copy-Item -LiteralPath $source -Destination $target}
                }
            }
        }
        Move-Item -LiteralPath $payload -Destination $destination
        [IO.File]::WriteAllText($marker,$checksum)
    }
    [IO.File]::WriteAllText((Join-Path $root 'current-version.txt'),$version)
    if($PrepareOnly){Write-Output ('Verified installation: '+$destination);return}
    Status 'Starting setup. Windows or Docker may request approval or a restart.'
    # Create a convenient repeat-launch shortcut alongside the installed versions.
    $start=Join-Path $root 'Start Python Trail.cmd'
    $startText='@echo off'+"`r`n"+'start "" powershell.exe -NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden -File "%~dp0'+$name+'\Setup-App.ps1" -AutoStart'+"`r`n"
    [IO.File]::WriteAllText($start,$startText,[Text.Encoding]::ASCII)
    $desktop=[Environment]::GetFolderPath('Desktop')
    if($desktop){
        try{$shell=New-Object -ComObject WScript.Shell;$shortcut=$shell.CreateShortcut((Join-Path $desktop 'Python Trail.lnk'));$shortcut.TargetPath=$start;$shortcut.WorkingDirectory=$root;$shortcut.Save()}catch{Write-Warning 'Could not create the desktop shortcut. Run the downloaded installer again to start the app.'}
    }
    $arguments='-NoProfile -ExecutionPolicy Bypass -STA -File "'+(Join-Path $destination 'Setup-App.ps1')+'" -AutoStart'
    Start-Process -FilePath (Join-Path $PSHOME 'powershell.exe') -ArgumentList $arguments -WindowStyle Hidden
}catch{
    if($window){[void][Windows.Forms.MessageBox]::Show(('Setup could not continue. Check your internet connection and that the GitHub repository is public, then try again.'+"`r`n`r`n"+$_.Exception.Message),'Python Trail setup')}
    throw
}finally{
    if($window){$window.Close();$window.Dispose()}
    if($scratch -and (Test-Path -LiteralPath $scratch)){Assert-Child $scratch;Remove-Item -LiteralPath $scratch -Recurse -Force}
}
