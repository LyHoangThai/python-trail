[CmdletBinding()]
param([switch]$CheckOnly)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[System.Windows.Forms.Application]::EnableVisualStyles()
$launcher=Join-Path $PSScriptRoot 'Launch-Sample.ps1'
if (-not (Test-Path -LiteralPath $launcher)) { throw 'Extract the complete ZIP before opening START HERE.' }
if ($CheckOnly) { Write-Output 'Setup window dependencies and launcher are ready.'; return }
$form=New-Object System.Windows.Forms.Form
$form.Text='Python Trail - Set up & play'
$form.ClientSize=New-Object System.Drawing.Size(680,500)
$form.StartPosition='CenterScreen'
$form.BackColor=[System.Drawing.Color]::FromArgb(246,248,241)
$form.Font=New-Object System.Drawing.Font('Segoe UI',10)
$form.MinimumSize=New-Object System.Drawing.Size(696,539)
$title=New-Object System.Windows.Forms.Label
$title.Text='Your next adventure starts here.'
$title.Font=New-Object System.Drawing.Font('Segoe UI',20,[System.Drawing.FontStyle]::Bold)
$title.SetBounds(26,23,625,45)
$intro=New-Object System.Windows.Forms.Label
$intro.Text='This button installs missing tools, starts the learning lab, and opens your browser. First setup needs internet. Windows or Docker may ask you to approve installation, finish setup, or restart.'
$intro.SetBounds(28,80,620,66)
$button=New-Object System.Windows.Forms.Button
$button.Text='Set up & open Python Trail'
$button.SetBounds(28,158,360,48)
$button.BackColor=[System.Drawing.Color]::FromArgb(202,233,166)
$button.FlatStyle='Flat'
$status=New-Object System.Windows.Forms.Label
$status.Text='Ready. Your saved work will be preserved.'
$status.SetBounds(28,221,620,43)
$log=New-Object System.Windows.Forms.TextBox
$log.Multiline=$true;$log.ReadOnly=$true;$log.ScrollBars='Vertical'
$log.SetBounds(28,274,620,155)
$log.Anchor='Top,Bottom,Left,Right'
$log.Font=New-Object System.Drawing.Font('Consolas',9)
$open=New-Object System.Windows.Forms.LinkLabel
$open.Text='Open lessons';$open.SetBounds(28,449,120,25);$open.Anchor='Bottom,Left'
$open.add_LinkClicked({Start-Process 'http://localhost:8766/learn'})
$folder=New-Object System.Windows.Forms.LinkLabel
$folder.Text='Open setup logs';$folder.SetBounds(165,449,150,25);$folder.Anchor='Bottom,Left'
$folder.add_LinkClicked({$path=Join-Path $PSScriptRoot 'setup-logs';if(Test-Path -LiteralPath $path){Start-Process explorer.exe -ArgumentList ('"'+$path+'"')}})
$form.Controls.AddRange(@($title,$intro,$button,$status,$log,$open,$folder))
$script:setupProcess=$null
$timer=New-Object System.Windows.Forms.Timer
$timer.Interval=800
$timer.add_Tick({
    try {
        $lines=@();foreach($path in @($script:outLog,$script:errLog)){if(Test-Path -LiteralPath $path){$lines+=Get-Content -LiteralPath $path -Tail 35 -ErrorAction SilentlyContinue}}
        $log.Text=($lines -join [Environment]::NewLine);$log.SelectionStart=$log.TextLength;$log.ScrollToCaret()
        if($script:setupProcess.HasExited){
            $timer.Stop();$script:setupProcess.WaitForExit();$button.Enabled=$true
            if($script:setupProcess.ExitCode -eq 0){$status.Text='Ready! Opening your learning lab. Use this same button next time.';$button.Text='Open / start Python Trail';Start-Process 'http://localhost:8766/learn'}
            else{$status.Text='Setup needs attention. Read the details below, finish Docker setup or restart if requested, then try again.';$button.Text='Try setup again'}
        }
    }catch{$timer.Stop();$button.Enabled=$true;$status.Text='Could not read setup progress: '+$_.Exception.Message}
})
$button.add_Click({
    try {
        $button.Enabled=$false;$status.Text='Setting up... First setup may take several minutes. Keep this window open.'
        $logs=Join-Path $PSScriptRoot 'setup-logs';[void][System.IO.Directory]::CreateDirectory($logs)
        $stamp=Get-Date -Format 'yyyyMMdd-HHmmss-fff'
        $script:outLog=Join-Path $logs ($stamp+'-output.txt');$script:errLog=Join-Path $logs ($stamp+'-errors.txt')
        $arguments='-NoProfile -ExecutionPolicy Bypass -File "'+$launcher+'" -NoOpen'
        $script:setupProcess=Start-Process -FilePath (Join-Path $PSHOME 'powershell.exe') -ArgumentList $arguments -WindowStyle Hidden -RedirectStandardOutput $script:outLog -RedirectStandardError $script:errLog -PassThru
        $timer.Start()
    }catch{$button.Enabled=$true;$status.Text='Setup could not start: '+$_.Exception.Message}
})
$form.add_FormClosing({param($sender,$eventArgs)
    if($script:setupProcess -and -not $script:setupProcess.HasExited){$eventArgs.Cancel=$true;[void][System.Windows.Forms.MessageBox]::Show('Setup is still running. Please wait for it to finish before closing this window.','Setup in progress')}
})
try{[void]$form.ShowDialog()}finally{$timer.Stop();$timer.Dispose();$form.Dispose()}
