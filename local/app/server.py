"""Local family learning dashboard and submission API."""
import json
import os
from pathlib import Path
import re
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT=Path(__file__).parent
QUEUE=Path(os.environ.get('TRAIL_QUEUE','/queue'))
LESSONS=json.loads((ROOT/'lessons.json').read_text(encoding='utf-8'))
BY_ID={q['id']:q for q in LESSONS}

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

    def job(self,job_id):
        with self.connect() as db:
            row=db.execute('SELECT result FROM jobs WHERE id=%s',(job_id,)).fetchone()
            return None if not row else row['result'] or {'status':'queued'}

    def pending(self):
        with self.connect() as db:
            return db.execute('SELECT id,quest,source FROM jobs WHERE result IS NULL ORDER BY created_at').fetchall()

    def progress(self):
        with self.connect() as db:
            active=db.execute('SELECT quest,updated_at::text FROM activity WHERE singleton=1').fetchone()
            done=db.execute('SELECT quest,completed_at::text FROM completed ORDER BY quest').fetchall()
            attempts=db.execute('SELECT quest,count(*)::integer AS count FROM jobs GROUP BY quest').fetchall()
            recent=db.execute('SELECT id,quest,result,created_at::text FROM jobs ORDER BY created_at DESC LIMIT 12').fetchall()
        return {'active':active,'completed':done,'attempts':attempts,'recent':recent}

class Service:
    def __init__(self,store,queue):
        self.store=store; self.queue=queue; self.lock=threading.Lock()
        queue.mkdir(exist_ok=True,parents=True)
        if os.name=='posix': os.chmod(queue,0o700)

    def enqueue(self,job):
        path=self.queue/(job['id']+'.job')
        payload={**job,'expected':BY_ID[job['quest']]['expected']}
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
                if route=='/api/lessons':
                    host_dir=os.environ.get('HOST_STUDENT_DIR','')
                    return self.response(200,{'lessons':[{k:v for k,v in q.items() if k!='solution'} for q in LESSONS], 'student_dir':host_dir})
                if route=='/api/progress': return self.response(200,service.store.progress())
                if route=='/api/solutions': return self.response(200,{q['id']:q['solution'] for q in LESSONS})
                if re.fullmatch(r'/api/jobs/[0-9a-f]{32}',route):
                    job=service.store.job(route.rsplit('/',1)[1])
                    return self.response(200 if job else 404,job or {'error':'Job not found'})
                if route in ('/','/index.html','/style.css','/dashboard.js'):
                    name='index.html' if route=='/' else route.lstrip('/')
                    types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8'}
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
                quest=data.get('quest')
                if type(quest)!=int or quest not in BY_ID: raise ValueError()
                route=urlparse(self.path).path
                if route=='/api/start': return self.response(200,service.start(quest))
                if route=='/api/submit':
                    source=data.get('source')
                    if not isinstance(source,str) or len(source)>32000: raise ValueError()
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
