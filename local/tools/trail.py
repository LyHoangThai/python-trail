"""Submit the active VS Code file; uses only Python's standard library."""
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API = os.environ.get('TRAIL_API', 'http://localhost:8765')

def request(path, data=None):
    req = Request(API + path, data=None if data is None else json.dumps(data).encode(),
                  headers={'Content-Type':'application/json', 'X-Trail-Client':'vscode'})
    with urlopen(req, timeout=10) as response:
        return json.load(response)

def resolve_assignment(path):
    path=Path(path).resolve()
    folder=path if path.is_dir() else path.parent
    metadata=folder/'lesson.json'
    if folder.parent.name!='lessons' or not metadata.is_file():
        raise ValueError('Open assignment.py or README.md inside lessons/NN_lesson_name/. Free play uses playground.py.')
    lesson=json.loads(metadata.read_text(encoding='utf-8'))
    quest=lesson.get('id')
    if type(quest)!=int or not 1<=quest<=9999 or not re.match(rf'^{quest:02d}_[a-z0-9_]+$',folder.name):
        raise ValueError('The lesson folder and lesson.json ID do not match.')
    assignment_name=lesson.get('assignment')
    if assignment_name not in ('assignment.py','assignment.st','assignment.ladder.json'): raise ValueError('The assignment filename in lesson.json is not supported.')
    assignment=folder/assignment_name
    if not assignment.is_file(): raise ValueError('This lesson is missing '+assignment_name+'.')
    return quest,assignment

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('start', 'check', 'submit'):
        print('Use: trail.py start|submit path/to/lessons/NN_lesson/assignment.py'); return 2
    try: quest,path=resolve_assignment(sys.argv[2])
    except (ValueError,OSError) as exc: print(exc); return 2
    if sys.argv[1] == 'start':
        result = request('/api/start', {'quest':quest})
        print(f"Now learning: {result['topic']} — {result['title']}"); return 0
    source = path.read_text(encoding='utf-8-sig')
    result = request('/api/submit', {'quest':quest, 'source':source})
    print(f"TURNED IN — lesson {quest:02d}\nSubmission ID: {result['id']}\nSaved file: {path.name}",flush=True)
    print('Your code snapshot is saved. Waiting for grading…',flush=True)
    for _ in range(180):
        status = request('/api/jobs/' + result['id'])
        if status['status'] == 'done':
            print('\nOUTPUT\n' + (status['output'] or '(no output)'))
            print('\n' + status['feedback'])
            print('Status: Completed' if status['passed'] else 'Status: Needs revision — your attempt is saved; edit and turn it in again.')
            print('\nParent dashboard: http://localhost:8765')
            return 0 if status['passed'] else 1
        time.sleep(0.5)
    print('Submission saved and still queued. Check its status in the parent dashboard before turning it in again.'); return 1

if __name__ == '__main__':
    try: sys.exit(main())
    except (OSError, URLError, HTTPError, ValueError) as exc:
        print(f'Could not reach Python Trail: {exc}\nStart it with: docker compose up -d'); sys.exit(1)
