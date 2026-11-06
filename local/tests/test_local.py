import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))
sys.path.insert(0,str(ROOT/'worker'))
import server
import worker

class MemoryStore:
    def __init__(self): self.jobs={};self.done=set();self.active=None
    def start(self,quest): self.active=quest
    def add(self,job): self.jobs[job['id']]={**job,'result':None}
    def finish(self,job_id,result):
        if job_id in self.jobs and self.jobs[job_id]['result'] is None:
            self.jobs[job_id]['result']=result
            if result['passed']: self.done.add(self.jobs[job_id]['quest'])
    def pending(self): return [j for j in self.jobs.values() if j['result'] is None]
    def job(self,job_id):
        j=self.jobs.get(job_id)
        return None if j is None else j['result'] or {'status':'queued'}
    def progress(self): return {'completed':[{'quest':q} for q in self.done],'active':self.active}

class LocalTests(unittest.TestCase):
    def job(self,lesson,source=None):
        return {'quest':lesson['id'],'source':lesson['solution'] if source is None else source,'expected':lesson['expected']}

    def test_all_reference_solutions(self):
        for lesson in server.LESSONS:
            with self.subTest(quest=lesson['id']):
                result=worker.grade(self.job(lesson),sandbox=False)
                self.assertTrue(result['passed'],result)

    def test_wrong_output_cannot_pass(self):
        result=worker.grade(self.job(server.LESSONS[0],'print("wrong")'),sandbox=False)
        self.assertFalse(result['passed'])

    def test_hardcoded_reward_fails_hidden_branches(self):
        source='score = 85\nif score >= 0:\n    print("Gold")'
        result=worker.grade(self.job(server.LESSONS[14],source),sandbox=False)
        self.assertFalse(result['passed']);self.assertIn('65',result['feedback'])

    def test_printing_list_output_without_loop_does_not_pass(self):
        source='print("map\\nsnack\\ntorch")'
        result=worker.grade(self.job(server.LESSONS[17],source),sandbox=False)
        self.assertFalse(result['passed'])

    def test_syntax_error_feedback(self):
        result=worker.grade(self.job(server.LESSONS[0],'if :'),sandbox=False)
        self.assertFalse(result['passed']);self.assertIn('SyntaxError',result['output'])

    def test_infinite_loop_is_stopped(self):
        result=worker.grade(self.job(server.LESSONS[0],'while True: pass'),sandbox=False)
        self.assertFalse(result['passed']);self.assertIn('5 seconds',result['feedback'])

    def test_queue_grade_and_progress(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=MemoryStore();service=server.Service(store,Path(tmp))
            lesson=server.LESSONS[20]
            submitted=service.submit(lesson['id'],lesson['solution'])
            self.assertEqual(store.active,21)
            path=Path(tmp)/(submitted['id']+'.job')
            queued=json.loads(path.read_text())
            self.assertEqual(queued['source'],lesson['solution'])
            result=worker.grade(queued,sandbox=False)
            path.unlink();path.with_suffix('.result').write_text(json.dumps(result))
            service.sync()
            self.assertEqual(store.done,{21})
            self.assertTrue(store.job(submitted['id'])['passed'])
            service.sync();self.assertEqual(len(store.done),1)

    def test_queue_recovery_preserves_submitted_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=MemoryStore();service=server.Service(store,Path(tmp))
            job={'id':uuid.uuid4().hex,'quest':1,'source':'print("draft saved")'}
            store.add(job);service.recover()
            saved=json.loads((Path(tmp)/(job['id']+'.job')).read_text())
            self.assertEqual(saved['source'],job['source'])

    def invoke(self,service,data,header=True,origin='http://localhost:8765',path='/api/submit'):
        handler=object.__new__(server.make_handler(service))
        body=json.dumps(data).encode()
        handler.headers={'Content-Length':str(len(body)),'Origin':origin}
        if header: handler.headers['X-Trail-Client']='browser'
        handler.rfile=io.BytesIO(body);handler.path=path
        result=[];handler.response=lambda *args:result.append(args)
        handler.do_POST();return result[0]

    def test_api_rejects_invalid_quests_and_foreign_websites(self):
        with tempfile.TemporaryDirectory() as tmp:
            service=server.Service(MemoryStore(),Path(tmp))
            self.assertEqual(self.invoke(service,{'quest':True,'source':''})[0],400)
            self.assertEqual(self.invoke(service,{'quest':26,'source':''})[0],400)
            self.assertEqual(self.invoke(service,{'quest':1,'source':''},header=False)[0],403)
            self.assertEqual(self.invoke(service,{'quest':1,'source':''},origin='https://example.com')[0],403)
            self.assertEqual(self.invoke(service,{'quest':1,'source':None})[0],400)
            self.assertEqual(self.invoke(service,{'quest':1,'source':'print("Hello, explorer!")'})[0],202)

    def test_all_starter_files_compile(self):
        for lesson in server.LESSONS:
            source=(ROOT/'student/quests'/lesson['filename']).read_text(encoding='utf-8')
            compile(source,lesson['filename'],'exec')

if __name__=='__main__':unittest.main()
