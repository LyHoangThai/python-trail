"""Single offline worker. No Docker socket, host workspace, or database credentials."""
import ast
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time

QUEUE = Path(os.environ.get('TRAIL_QUEUE', '/queue'))

def restrict():
    import resource
    resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
    resource.setrlimit(resource.RLIMIT_AS, (128*1024*1024, 128*1024*1024))
    resource.setrlimit(resource.RLIMIT_FSIZE, (65536, 65536))
    resource.setrlimit(resource.RLIMIT_NPROC, (16, 16))
    resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    os.setgroups([])
    os.setgid(65534)
    os.setuid(65534)

def execute(source, sandbox=True, inputs=''):
    # sandbox=False exists for functional tests on Windows, never for the server.
    with tempfile.TemporaryDirectory() as tmp:
        if sandbox: os.chmod(tmp, 0o777)
        with tempfile.TemporaryFile() as output:
            process = subprocess.Popen([sys.executable, '-I', '-B', '-c', source],
                cwd=tmp, stdin=subprocess.PIPE, stdout=output, stderr=output,
                env={'PATH':'/usr/local/bin:/usr/bin:/bin','HOME':tmp},
                start_new_session=True if sandbox else False,
                preexec_fn=restrict if sandbox else None)
            timed_out=False
            try: process.communicate(input=inputs.encode('utf-8'),timeout=5)
            except subprocess.TimeoutExpired:
                timed_out=True
                if sandbox: os.killpg(process.pid, signal.SIGKILL)
                else: process.kill()
                process.wait()
            finally:
                if sandbox:
                    try: os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError: pass
            output.seek(0)
            text=output.read(65536).decode('utf-8', errors='replace').replace('\r\n','\n')
            error='Stopped after 5 seconds. Check for a loop that never ends.' if timed_out else ('Python exited with an error. Read the output above.' if process.returncode else '')
            return text,error

from rubric import requirement, cases

# Kept as a public helper for the regression tests and local diagnostics.
def technique(source, quest):
    return requirement(source, quest)

def grade(job, sandbox=True):
    source=job['source']
    output,error=execute(source,sandbox,job.get('inputs',''))
    if job.get('mode')=='run':
        return {'status':'done','output':output,'passed':not bool(error),'feedback':error or 'Code ran successfully. Turn in your assignment when you are ready.'}
    result={'status':'done','output':output,'passed':False,'feedback':error}
    if error: return result
    try: clue=technique(source,job['quest'])
    except SyntaxError: clue='Check your Python syntax.'
    if clue: result['feedback']=clue; return result
    if output.strip()!=job['expected'].strip():
        result['feedback']='Keep going! Compare your output with the mission, including spelling and line breaks.'; return result
    for changed_source,expected,clue in cases(source,job['quest']):
        if changed_source is None:
            result['feedback']='Keep and use the lesson variables so we can check changed inputs.'
            return result
        changed_output,changed_error=execute(changed_source,sandbox)
        if changed_error or changed_output.strip()!=expected.strip():
            result['feedback']=clue
            return result
    result.update(passed=True,feedback='Quest complete! Your progress is saved. Try your own variation next.')
    return result

def main():
    QUEUE.mkdir(exist_ok=True,mode=0o700)
    os.chmod(QUEUE,0o700)
    # Resume interrupted work after a container restart.
    for pending in QUEUE.glob('*.running'):
        pending.rename(pending.with_suffix('.job'))
    print('Offline grading worker ready.',flush=True)
    while True:
        for path in sorted(QUEUE.glob('*.job')):
            running=path.with_suffix('.running')
            try:
                path.rename(running)
                job=json.loads(running.read_text())
                result=grade(job)
            except Exception:
                result={'status':'done','output':'','passed':False,'feedback':'The worker encountered a problem. Check worker logs and retry.'}
            temporary=path.with_suffix('.tmp')
            temporary.write_text(json.dumps(result))
            temporary.replace(path.with_suffix('.result'))
            running.unlink(missing_ok=True)
        time.sleep(.2)

if __name__=='__main__': main()
