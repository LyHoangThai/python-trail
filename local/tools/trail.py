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

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('start', 'check'):
        print('Use: trail.py start|check path/to/quest.py'); return 2
    path = Path(sys.argv[2])
    match = re.fullmatch(r'(\d{2})_[a-z0-9_]+\.py', path.name)
    if not match or path.parent.name != 'quests':
        print('Open a file in quests/ to check a quest. Run playground.py with Ctrl+Shift+B.'); return 2
    quest = int(match[1])
    if sys.argv[1] == 'start':
        result = request('/api/start', {'quest':quest})
        print(f"Now learning: {result['topic']} — {result['title']}"); return 0
    source = path.read_text(encoding='utf-8-sig')
    result = request('/api/submit', {'quest':quest, 'source':source})
    print('Checking your code in the worker…')
    for _ in range(180):
        status = request('/api/jobs/' + result['id'])
        if status['status'] == 'done':
            print('\nOUTPUT\n' + (status['output'] or '(no output)'))
            print('\n' + status['feedback'])
            print('\nParent dashboard: http://localhost:8765')
            return 0 if status['passed'] else 1
        time.sleep(0.5)
    print('Still queued. Check Docker Desktop and the worker logs, then retry.'); return 1

if __name__ == '__main__':
    try: sys.exit(main())
    except (OSError, URLError, HTTPError, ValueError) as exc:
        print(f'Could not reach Python Trail: {exc}\nStart it with: docker compose up -d'); sys.exit(1)
