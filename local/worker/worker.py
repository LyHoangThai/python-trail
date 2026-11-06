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

def technique(source, quest):
    tree=ast.parse(source)
    nodes=list(ast.walk(tree))
    required={11:ast.If,12:ast.If,13:ast.If,14:ast.BoolOp,15:ast.If,
              16:ast.For,17:ast.For,18:ast.For,19:ast.FunctionDef,20:ast.FunctionDef,
              21:ast.Dict,22:ast.Dict,23:ast.Dict,24:ast.For,25:ast.FunctionDef}
    kind=required.get(quest)
    if kind and not any(isinstance(n,kind) for n in nodes):
        return 'Use the Python technique described in the mission.'
    if quest in (6,7) and not any(isinstance(n,ast.Assign) for n in nodes):
        return 'Store the value in a variable before printing.'
    if quest==4 and '#' not in source: return 'Include a comment starting with #.'
    if quest==8 and not any(isinstance(n,ast.JoinedStr) for n in nodes): return 'Use an f-string.'
    if quest==9 and not all(any(isinstance(n,k) for n in nodes) for k in (ast.FloorDiv,ast.Mod)):
        return 'Use // and % to calculate shares and leftovers.'
    return ''

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
    if job['quest']==15:
        tree=ast.parse(source)
        assignment=next((n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='score' for t in n.targets)),None)
        if not assignment: result['feedback']='Start by assigning score = 85.'; return result
        for score,expected in [(65,'Silver'),(20,'Bronze')]:
            assignment.value=ast.Constant(score)
            text,error=execute(ast.unparse(ast.fix_missing_locations(tree)),sandbox)
            if error or text.strip()!=expected:
                result['feedback']=f'Try score = {score}. It should print {expected}.'; return result
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
