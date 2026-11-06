"""Local family learning dashboard and submission API."""
import json
import difflib
import os
from pathlib import Path
import re
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

ROOT=Path(__file__).parent
QUEUE=Path(os.environ.get('TRAIL_QUEUE','/queue'))
LESSONS=json.loads((ROOT/'lessons.json').read_text(encoding='utf-8'))
BY_ID={q['id']:q for q in LESSONS}
SUBJECTS=json.loads((ROOT/'subjects.json').read_text(encoding='utf-8'))

class Store:
    def connect(self):
        import psycopg
        from psycopg.rows import dict_row
        return psycopg.connect(host='db',dbname='trail',user='trail',password=os.environ['DB_PASSWORD'],row_factory=dict_row)

    def initialize(self):
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS activity (singleton integer PRIMARY KEY CHECK(singleton=1), quest integer, updated_at timestamptz DEFAULT now())')
            db.execute("CREATE TABLE IF NOT EXISTS jobs (id text PRIMARY KEY, quest integer NOT NULL, source text NOT NULL, result jsonb, created_at timestamptz DEFAULT now())")
            db.execute('CREATE TABLE IF NOT EXISTS completed (quest integer PRIMARY KEY, completed_at timestamptz DEFAULT now())')
            db.execute('CREATE INDEX IF NOT EXISTS jobs_quest_history ON jobs(quest,created_at,id)')
            db.execute('CREATE TABLE IF NOT EXISTS drafts (quest integer PRIMARY KEY, source text NOT NULL, updated_at timestamptz DEFAULT now())')
            db.execute('CREATE TABLE IF NOT EXISTS executions (id text PRIMARY KEY, quest integer NOT NULL, source text NOT NULL, inputs text NOT NULL DEFAULT \'\', result jsonb, created_at timestamptz DEFAULT now())')

    def start(self,quest):
        with self.connect() as db:
            db.execute('INSERT INTO activity(singleton,quest) VALUES(1,%s) ON CONFLICT(singleton) DO UPDATE SET quest=excluded.quest, updated_at=now()',(quest,))

    def add(self,job):
        with self.connect() as db:
            db.execute('INSERT INTO jobs(id,quest,source) VALUES(%s,%s,%s)',(job['id'],job['quest'],job['source']))

    def finish(self,job_id,result):
        with self.connect() as db:
            row=db.execute('UPDATE jobs SET result=%s::jsonb WHERE id=%s AND result IS NULL RETURNING quest',(json.dumps(result),job_id)).fetchone()
            if row and result['passed']:
                db.execute('INSERT INTO completed(quest) VALUES(%s) ON CONFLICT DO NOTHING',(row['quest'],))
            if not row:
                db.execute('UPDATE executions SET result=%s::jsonb WHERE id=%s AND result IS NULL',(json.dumps(result),job_id))

    def job(self,job_id):
        with self.connect() as db:
            row=db.execute('SELECT result FROM jobs WHERE id=%s',(job_id,)).fetchone()
            return None if not row else row['result'] or {'status':'queued'}

    def pending(self):
        with self.connect() as db:
            jobs=db.execute("SELECT id,quest,source,'submit' AS mode FROM jobs WHERE result IS NULL ORDER BY created_at").fetchall()
            runs=db.execute("SELECT id,quest,source,inputs,'run' AS mode FROM executions WHERE result IS NULL ORDER BY created_at").fetchall()
            return jobs+runs

    def draft(self,quest):
        with self.connect() as db:
            row=db.execute('SELECT source,updated_at::text FROM drafts WHERE quest=%s',(quest,)).fetchone()
        return row or {'source':BY_ID[quest]['starter'] if quest else '# Try an idea!\nprint("Hello, imagination!")\n','updated_at':None}

    def save_draft(self,quest,source):
        with self.connect() as db:
            db.execute('INSERT INTO drafts(quest,source) VALUES(%s,%s) ON CONFLICT(quest) DO UPDATE SET source=excluded.source,updated_at=now()',(quest,source))

    def add_run(self,job):
        with self.connect() as db:
            db.execute('INSERT INTO executions(id,quest,source,inputs) VALUES(%s,%s,%s,%s)',(job['id'],job['quest'],job['source'],job['inputs']))

    def run_job(self,job_id):
        with self.connect() as db:
            row=db.execute('SELECT result FROM executions WHERE id=%s',(job_id,)).fetchone()
        return None if row is None else row['result'] or {'status':'queued'}

    def progress(self):
        with self.connect() as db:
            active=db.execute('SELECT quest,updated_at::text FROM activity WHERE singleton=1').fetchone()
            done=db.execute('SELECT quest,completed_at::text FROM completed ORDER BY quest').fetchall()
            attempts=db.execute('SELECT quest,count(*)::integer AS count FROM jobs GROUP BY quest').fetchall()
            recent=db.execute('SELECT id,quest,result,created_at::text FROM jobs ORDER BY created_at DESC LIMIT 12').fetchall()
        return {'active':active,'completed':done,'attempts':attempts,'recent':recent}

    def history(self,quest=None,offset=0,limit=20):
        with self.connect() as db:
            rows=db.execute('''WITH ranked AS (
                SELECT id,quest,result,created_at,row_number() OVER(PARTITION BY quest ORDER BY created_at,id) AS attempt
                FROM jobs WHERE (%s::integer IS NULL OR quest=%s))
                SELECT id,quest,result,created_at::text,attempt FROM ranked
                ORDER BY created_at DESC,id DESC LIMIT %s OFFSET %s''',(quest,quest,limit,offset)).fetchall()
            total=db.execute('SELECT count(*) AS total FROM jobs WHERE (%s::integer IS NULL OR quest=%s)',(quest,quest)).fetchone()['total']
        return {'submissions':rows,'total':total,'offset':offset,'limit':limit}

    def submission(self,job_id):
        with self.connect() as db:
            row=db.execute('SELECT id,quest,source,result,created_at::text FROM jobs WHERE id=%s',(job_id,)).fetchone()
            if not row: return None
            previous=db.execute('''SELECT id,source,created_at::text FROM jobs
                WHERE quest=%s AND (created_at,id)<(%s::timestamptz,%s)
                ORDER BY created_at DESC,id DESC LIMIT 1''',(row['quest'],row['created_at'],row['id'])).fetchone()
            attempt=db.execute('''SELECT count(*) AS attempt FROM jobs
                WHERE quest=%s AND (created_at,id)<=(%s::timestamptz,%s)''',(row['quest'],row['created_at'],row['id'])).fetchone()['attempt']
        row['previous']=previous
        row['attempt']=attempt
        return row

class Service:
    def __init__(self,store,queue):
        self.store=store; self.queue=queue; self.lock=threading.Lock()
        queue.mkdir(exist_ok=True,parents=True)
        if os.name=='posix': os.chmod(queue,0o700)

    def enqueue(self,job):
        path=self.queue/(job['id']+'.job')
        payload={**job,'expected':None if job.get('mode')=='run' else BY_ID[job['quest']]['expected']}
        tmp=path.with_suffix('.writing')
        tmp.write_text(json.dumps(payload),encoding='utf-8');tmp.replace(path)

    def sync(self):
        with self.lock:
            for result_file in self.queue.glob('*.result'):
                try:
                    result=json.loads(result_file.read_text())
                    self.store.finish(result_file.stem,result)
                    result_file.unlink()
                except (OSError,ValueError): continue

    def recover(self):
        for job in self.store.pending():
            if not any((self.queue/(job['id']+ext)).exists() for ext in ('.job','.running','.result')):
                self.enqueue(job)

    def start(self,quest):
        self.store.start(quest)
        return {'title':BY_ID[quest]['title'],'topic':BY_ID[quest]['topic']}

    def submit(self,quest,source):
        job={'id':uuid.uuid4().hex,'quest':quest,'source':source}
        self.store.add(job);self.start(quest);self.enqueue(job)
        return {'id':job['id']}

    def run(self,quest,source,inputs=''):
        job={'id':uuid.uuid4().hex,'quest':quest,'source':source,'inputs':inputs,'mode':'run'}
        self.store.add_run(job);self.enqueue(job)
        return {'id':job['id']}

    def submission(self,job_id):
        row=self.store.submission(job_id)
        if not row: return None
        previous=row['previous']
        baseline=previous['source'] if previous else BY_ID[row['quest']]['starter']
        row['baseline_label']='Previous submission' if previous else 'Lesson starter'
        row['baseline_source']=baseline
        suffix=Path(BY_ID[row['quest']]['assignment_path']).suffix
        row['diff']='\n'.join(difflib.unified_diff(baseline.splitlines(),row['source'].splitlines(),fromfile=('previous' if previous else 'starter')+suffix,tofile='submitted'+suffix,lineterm=''))
        return row

def make_handler(service):
    class Handler(BaseHTTPRequestHandler):
        def response(self,status,data,content_type='application/json'):
            body=json.dumps(data).encode() if content_type=='application/json' else data
            self.send_response(status)
            self.send_header('Content-Type',content_type)
            self.send_header('Content-Length',str(len(body)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.end_headers();self.wfile.write(body)

        def do_GET(self):
            try:
                route=urlparse(self.path).path
                if route=='/api/health':
                    with service.store.connect() as db: db.execute('SELECT 1')
                    return self.response(200,{'ok':True})
                service.sync()
                if route=='/api/subjects': return self.response(200,{'subjects':SUBJECTS})
                if route=='/api/lessons':
                    host_dir=os.environ.get('HOST_STUDENT_DIR','')
                    return self.response(200,{'lessons':[{k:v for k,v in q.items() if k!='solution'} for q in LESSONS], 'student_dir':host_dir})
                if route=='/api/progress': return self.response(200,service.store.progress())
                if re.fullmatch(r'/api/drafts/\d+',route):
                    quest=int(route.rsplit('/',1)[1])
                    if quest not in BY_ID and quest!=0: return self.response(404,{'error':'Lesson not found'})
                    return self.response(200,service.store.draft(quest))
                if re.fullmatch(r'/api/runs/[0-9a-f]{32}',route):
                    result=service.store.run_job(route.rsplit('/',1)[1])
                    return self.response(200 if result else 404,result or {'error':'Run not found'})
                if route=='/api/solutions': return self.response(200,{q['id']:q['solution'] for q in LESSONS})
                if route=='/api/submissions':
                    query=parse_qs(urlparse(self.path).query)
                    try:
                        quest=int(query['quest'][0]) if 'quest' in query else None
                        offset=int(query.get('offset',['0'])[0])
                        if (quest is not None and quest not in BY_ID) or offset<0: raise ValueError()
                    except (ValueError,IndexError): return self.response(400,{'error':'Choose a valid lesson and history page.'})
                    return self.response(200,service.store.history(quest,offset))
                if re.fullmatch(r'/api/submissions/[0-9a-f]{32}',route):
                    submission=service.submission(route.rsplit('/',1)[1])
                    return self.response(200 if submission else 404,submission or {'error':'Submission not found'})
                if re.fullmatch(r'/api/jobs/[0-9a-f]{32}',route):
                    job=service.store.job(route.rsplit('/',1)[1])
                    return self.response(200 if job else 404,job or {'error':'Job not found'})
                if route in ('/','/index.html'):
                    self.send_response(302);self.send_header('Location','/learn');self.send_header('Content-Length','0');self.end_headers();return
                pages={'/learn':'learn.html','/parent':'parent.html','/playground':'lesson.html'}
                if re.fullmatch(r'/lessons/\d+',route) and int(route.rsplit('/',1)[1]) in BY_ID: pages[route]='lesson.html'
                if re.fullmatch(r'/parent/submissions/[0-9a-f]{32}',route): pages[route]='submission.html'
                assets=('/style.css','/app.css','/parent.js','/student.js','/learn.js','/review.js','/helper.js','/helper.json','/plc.js','/plc-helper.json','/ladder-model.js')
                if route in pages or route in assets:
                    name=pages.get(route,route.lstrip('/'))
                    types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8'}
                    return self.response(200,(ROOT/'static'/name).read_bytes(),types[Path(name).suffix])
                self.response(404,{'error':'Not found'})
            except Exception:
                self.response(503,{'error':'Local services are not ready. Check docker compose logs app db.'})

        def do_POST(self):
            # A cross-origin website cannot make submissions with this custom header.
            origin=self.headers.get('Origin')
            if self.headers.get('X-Trail-Client') not in ('browser','vscode') or (origin and origin not in ('http://localhost:8765','http://127.0.0.1:8765')):
                return self.response(403,{'error':'Open the local dashboard to continue.'})
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=40000: return self.response(413,{'error':'Submission is too large.'})
                data=json.loads(self.rfile.read(length))
                if not isinstance(data,dict): raise ValueError()
                route=urlparse(self.path).path
                quest=data.get('quest')
                if type(quest)!=int or (quest not in BY_ID and not (quest==0 and route in ('/api/drafts','/api/run'))): raise ValueError()
                if route=='/api/start': return self.response(200,service.start(quest))
                if route in ('/api/submit','/api/drafts','/api/run'):
                    source=data.get('source')
                    if not isinstance(source,str) or len(source)>32000: raise ValueError()
                    if route=='/api/drafts':
                        service.store.save_draft(quest,source)
                        return self.response(200,{'saved':True})
                    if route=='/api/run':
                        inputs=data.get('inputs','')
                        if not isinstance(inputs,str) or len(inputs)>4000: raise ValueError()
                        return self.response(202,service.run(quest,source,inputs))
                    return self.response(202,service.submit(quest,source))
                self.response(404,{'error':'Not found'})
            except (ValueError,TypeError): self.response(400,{'error':'Choose a valid quest and Python file.'})
            except Exception: self.response(503,{'error':'Could not save the submission. Check local services.'})

        def log_message(self,format,*args):
            if '/api/progress' not in self.path: super().log_message(format,*args)
    return Handler

if __name__=='__main__':
    store=Store();store.initialize()
    service=Service(store,QUEUE);service.recover()
    print('Python Trail ready on port 8000',flush=True)
    ThreadingHTTPServer(('0.0.0.0',8000),make_handler(service)).serve_forever()
