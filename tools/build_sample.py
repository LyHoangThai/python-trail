"""Build a credential-free sample distribution from explicit source files."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
VERSION='0.1.2'
NAME=f'python-trail-sample-{VERSION}'
OUT=ROOT/'releases'/NAME
if OUT.exists():raise SystemExit(f'{OUT} already exists; use a new version or output folder.')
OUT.mkdir(parents=True)
TEXT={'.py','.js','.cjs','.css','.html','.json','.md','.ps1','.yml','.txt'}
def write(relative,data):
    target=OUT/relative;target.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(data,str):target.write_text(data.replace('8765','8766').replace('python-trail-local','python-trail-sample'),encoding='utf-8')
    else:target.write_bytes(data)
def copy(source,relative=None):
    relative=relative or source.relative_to(ROOT)
    write(relative,source.read_text(encoding='utf-8-sig') if source.suffix in TEXT or source.name.startswith('.') or source.name=='Dockerfile' else source.read_bytes())
for folder in ['app','worker','playground','tools','tests']:
    for source in (ROOT/'local'/folder).rglob('*'):
        if source.is_file() and '__pycache__' not in source.parts and source.suffix not in ('.pyc','.pyo') and not source.name.startswith('.env'):
            copy(source)
for name in ['compose.yml','setup.ps1','start.ps1','stop.ps1','backup.ps1','smoke-test.ps1','.gitignore','README.md']:
    copy(ROOT/'local'/name)
for folder in ['.devcontainer','.vscode']:
    for source in (ROOT/'local/student'/folder).glob('*'):
        if source.is_file():copy(source)
for name in ['README.md','lessons/README.md']:copy(ROOT/'local/student'/name)
write('local/student/playground.py','# Try your own Python idea here.\nprint("Hello, explorer!")\n')
lessons=json.loads((ROOT/'local/app/lessons.json').read_text(encoding='utf-8'))
for lesson in lessons:
    directory=ROOT/'local/student'/lesson['directory']
    for name in ['README.md','lesson.json']:copy(directory/name)
    write(Path('local/student')/lesson['assignment_path'],lesson['starter'].rstrip()+'\n')
for name in ['PLC.md','GRADING.md']:copy(ROOT/name)
copy(ROOT/'plc-studio.png',Path('preview/plc-studio.png'))
for source in (ROOT/'product').rglob('*'):
    if source.is_file():
        target=OUT/source.relative_to(ROOT/'product');target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())
# Correct the older source guide's path summary in the packaged guide.
p=OUT/'local/README.md';s=p.read_text(encoding='utf-8').replace('A free local Python learning lab with 53 lessons.','A local learning lab with 45 Python lessons and 8 PLC lessons.').replace('## Six learning paths','## Separate Python and PLC subjects').replace('The home page has Beginner (25 lessons), Intermediate (5), Advanced (5), Algorithms (5), Data Structures (5), and PLC (8).','Choose Python or PLC from the home dropdown. Python has Beginner (25 lessons), Intermediate (5), Advanced (5), Algorithms (5), and Data Structures (5). PLC has Ladder Logic (4) and Structured Text (4).');p.write_text(s,encoding='utf-8')
entries=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file():entries.append({'path':p.relative_to(OUT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
manifest={'product':'Python Trail — Python & PLC Sample','version':VERSION,'edition':'sample','port':8766,'compose_project':'python-trail-sample','lessons':{'python':45,'plc':8},'files':entries}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
assert len(list((OUT/'local/student/lessons').glob('*/lesson.json')))==53
assert not list(OUT.rglob('.env'))
for lesson in lessons:assert (OUT/'local/student'/lesson['assignment_path']).read_text(encoding='utf-8').rstrip()==lesson['starter'].rstrip()
archive=OUT.parent/(NAME+'.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,Path(NAME)/p.relative_to(OUT))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
checksum=hashlib.sha256(archive.read_bytes()).hexdigest()
(archive.parent/(archive.name+'.sha256')).write_text(checksum+'  '+archive.name+'\n',encoding='utf-8')
print(json.dumps({'folder':str(OUT),'archive':str(archive),'files':len(entries)+1,'sha256':checksum},indent=2))
