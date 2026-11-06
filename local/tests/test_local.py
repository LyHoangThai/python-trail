import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import uuid
from unittest.mock import Mock

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))
sys.path.insert(0,str(ROOT/'worker'))
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT.parent/'tools'))
import server
import worker
from plc import parse_st, ladder
import trail
from lesson_layout import create_lesson

class MemoryStore:
    def __init__(self): self.jobs={};self.runs={};self.drafts={};self.done=set();self.active=None
    def start(self,quest): self.active=quest
    def add(self,job): self.jobs[job['id']]={**job,'result':None}
    def finish(self,job_id,result):
        if job_id in self.jobs and self.jobs[job_id]['result'] is None:
            self.jobs[job_id]['result']=result
            if result['passed']: self.done.add(self.jobs[job_id]['quest'])
        elif job_id in self.runs: self.runs[job_id]['result']=result
    def add_run(self,job): self.runs[job['id']]={**job,'result':None}
    def save_draft(self,quest,source): self.drafts[quest]=source
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
        self.assertFalse(result['passed']);self.assertIn('elif',result['feedback'])

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
            self.assertEqual(self.invoke(service,{'quest':9999,'source':''})[0],400)
            self.assertEqual(self.invoke(service,{'quest':1,'source':''},header=False)[0],403)
            self.assertEqual(self.invoke(service,{'quest':1,'source':''},origin='https://example.com')[0],403)
            self.assertEqual(self.invoke(service,{'quest':1,'source':None})[0],400)
            self.assertEqual(self.invoke(service,{'quest':1,'source':'print("Hello, explorer!")'})[0],202)

    def test_all_starter_files_compile(self):
        for lesson in server.LESSONS:
            source=(ROOT/'student'/lesson['assignment_path']).read_text(encoding='utf-8')
            if lesson.get('engine')=='plc-st':parse_st(source)
            elif lesson.get('engine')=='plc-ladder':ladder(source,{'SW1':False,'SW2':False})
            else:compile(source,lesson['assignment_path'],'exec')

    def test_every_lesson_has_exact_folder_and_submission_identity(self):
        folders=list((ROOT/'student/lessons').glob('*/lesson.json'))
        self.assertEqual(len(folders),len(server.LESSONS))
        for lesson in server.LESSONS:
            assignment=ROOT/'student'/lesson['assignment_path']
            self.assertEqual(trail.resolve_assignment(assignment),(lesson['id'],assignment.resolve()))
            self.assertEqual(trail.resolve_assignment(assignment.parent/'README.md'),(lesson['id'],assignment.resolve()))

    def test_migration_preserves_student_code_and_generator_rerun(self):
        with tempfile.TemporaryDirectory() as tmp:
            student=Path(tmp);(student/'quests').mkdir()
            lesson=dict(server.LESSONS[0]);original=b'# my saved work\nprint("I made this")\n'
            (student/'quests'/lesson['filename']).write_bytes(original)
            assignment=create_lesson(lesson,student)
            self.assertEqual(assignment.read_bytes(),original)
            self.assertFalse((student/'quests'/lesson['filename']).exists())
            create_lesson(lesson,student)
            self.assertEqual(assignment.read_bytes(),original)

    def test_submission_identity_rejects_mismatched_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            lesson=dict(server.LESSONS[0]);assignment=create_lesson(lesson,Path(tmp))
            metadata=assignment.parent/'lesson.json'
            data=json.loads(metadata.read_text());data['id']=2;metadata.write_text(json.dumps(data))
            with self.assertRaises(ValueError): trail.resolve_assignment(assignment)

    def test_history_compares_saved_snapshots_and_handles_missing_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=Mock();service=server.Service(store,Path(tmp))
            previous={'id':'a'*32,'source':'print("old")','created_at':'2026-11-06T10:00:00Z'}
            store.submission.return_value={'id':'b'*32,'quest':1,'source':'print("new")','previous':previous,'attempt':2}
            result=service.submission('b'*32)
            self.assertEqual(result['source'],'print("new")')
            self.assertEqual(result['baseline_source'],'print("old")')
            self.assertIn('-print("old")\n+print("new")',result['diff'])
            self.assertEqual(result['baseline_label'],'Previous submission')

    def test_first_submission_compares_with_its_lesson_starter(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=Mock();service=server.Service(store,Path(tmp))
            lesson=server.LESSONS[20]
            store.submission.return_value={'id':'c'*32,'quest':21,'source':lesson['solution'],'previous':None,'attempt':1}
            result=service.submission('c'*32)
            self.assertEqual(result['baseline_source'],lesson['starter'])
            self.assertEqual(result['baseline_label'],'Lesson starter')
            store.submission.return_value=None
            self.assertIsNone(service.submission('0'*32))

    def test_run_executes_without_creating_turnin_or_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=MemoryStore();service=server.Service(store,Path(tmp))
            submitted=service.run(0,'name = input("Name? ")\nprint("Hi", name)','Pip\n')
            path=Path(tmp)/(submitted['id']+'.job')
            job=json.loads(path.read_text())
            self.assertIsNone(job['expected'])
            result=worker.grade(job,sandbox=False)
            self.assertTrue(result['passed'],result)
            self.assertIn('Hi Pip',result['output'])
            path.unlink();path.with_suffix('.result').write_text(json.dumps(result))
            service.sync()
            self.assertFalse(store.jobs)
            self.assertFalse(store.done)

    def test_browser_routes_serve_different_functional_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            service=server.Service(MemoryStore(),Path(tmp))
            for path,expected,absent in [('/learn',b'Your learning trail',b'id="history"'),('/lessons/1',b'Python code editor',b'id="history"'),('/parent',b'Submission history',b'Python code editor'),('/parent/submissions/'+'a'*32,b'Submitted code',b'Python code editor'),('/playground',b'Python code editor',b'id="history"')]:
                handler=object.__new__(server.make_handler(service));handler.path=path
                result=[];handler.response=lambda *args:result.append(args)
                handler.do_GET()
                self.assertEqual(result[0][0],200,path)
                self.assertIn(expected,result[0][1],path)
                self.assertNotIn(absent,result[0][1],path)

    def test_draft_endpoint_accepts_playground_without_recording_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=MemoryStore();service=server.Service(store,Path(tmp))
            result=self.invoke(service,{'quest':0,'source':'print("draft")'},path='/api/drafts')
            self.assertEqual(result[0],200)
            self.assertEqual(store.drafts[0],'print("draft")')
            self.assertFalse(store.jobs)

if __name__=='__main__':unittest.main()
