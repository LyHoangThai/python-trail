from pathlib import Path
import hashlib,json
root=Path.cwd();version='0.1.2'
archive=root/'releases'/f'python-trail-sample-{version}.zip'
(root/'distribution/channel.json').write_text(json.dumps({'version':version,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
loader='''@echo off
setlocal
set "PYTHON_TRAIL_INSTALLER=%~f0"
start "" powershell.exe -NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden -Command "$lines=[IO.File]::ReadAllLines($env:PYTHON_TRAIL_INSTALLER); $i=[Array]::IndexOf($lines,'#--POWERSHELL--'); if($i -lt 0){throw 'Installer is incomplete'}; & ([scriptblock]::Create(($lines[($i+1)..($lines.Length-1)] -join [Environment]::NewLine)))"
exit /b
#--POWERSHELL--
'''
body=(root/'distribution/bootstrap.ps1').read_text(encoding='utf-8-sig')
(root/'Install-Python-Trail.cmd').write_bytes((loader+body).replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
print('Built single-file installer and versioned channel.')
