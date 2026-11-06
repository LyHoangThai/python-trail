import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'worker'))
from plc import PLC_LESSONS,PLCError,parse_st,st_scan,ladder,grade_plc,diagram,NO,NC
from worker import grade

class PLCTests(unittest.TestCase):
    def test_all_eight_lessons_check_all_input_combinations(self):
        for lesson in PLC_LESSONS:
            with self.subTest(lesson=lesson['id']):
                result=grade({'quest':lesson['id'],'source':lesson['solution']})
                self.assertTrue(result['passed'],result)
                self.assertEqual(result['output'].count('✓'),4)

    def test_constants_cannot_pass_switch_following_lessons(self):
        for lesson in PLC_LESSONS:
            for value in [False,True]:
                source=diagram([[]] if value else []) if lesson['engine']=='plc-ladder' else 'LAMP := '+str(value).upper()+';'
                with self.subTest(lesson=lesson['id'],value=value):self.assertFalse(grade({'quest':lesson['id'],'source':source})['passed'])

    def test_unconnected_coil_and_malformed_diagrams(self):
        source=json.dumps({'branches':[[NO('SW1')]],'coil':None})
        self.assertFalse(ladder(source,{'SW1':True,'SW2':False}))
        result=grade({'quest':46,'source':source})
        self.assertFalse(result['passed']);self.assertIn('coil',result['feedback'])
        for source in ['[]','null','not JSON']:
            self.assertFalse(grade({'quest':46,'source':source})['passed'])

    def test_series_parallel_and_closed_contacts(self):
        inputs={'SW1':True,'SW2':False}
        self.assertFalse(ladder(diagram([[NO('SW1'),NO('SW2')]]),inputs))
        self.assertTrue(ladder(diagram([[NO('SW1')],[NO('SW2')]]),inputs))
        self.assertFalse(ladder(diagram([[NC('SW1')]]),inputs))
        self.assertTrue(ladder(diagram([[NC('SW2')]]),inputs))

    def test_structured_text_precedence_comments_case_and_if(self):
        source='(* pretend lamp *)\nif not sw1 or sw2 and FALSE then\n lamp := true;\nelse\n lamp := false;\nend_if; // end'
        program=parse_st(source)
        self.assertTrue(st_scan(program,{'SW1':False,'SW2':True}))
        self.assertFalse(st_scan(program,{'SW1':True,'SW2':True}))

    def test_st_lesson_requires_its_taught_construct(self):
        self.assertFalse(grade({'quest':53,'source':'LAMP := NOT SW1;'})['passed'])

    def test_invalid_st_cannot_write_inputs_or_run_arbitrary_code(self):
        for source in ['SW1 := TRUE;','import os','LAMP = TRUE;','WHILE TRUE DO END_WHILE;','IF SW1 THEN LAMP := TRUE;','LAMP := open("file");']:
            with self.subTest(source=source):
                with self.assertRaises(PLCError):parse_st(source)

    def test_ladder_bounds_and_unknown_signals(self):
        for source in [diagram([[{'input':'SW3','contact':'NO'}]]),diagram([[{'input':'SW1','contact':'BAD'}]]),diagram([[NO('SW1')]*5]),diagram([[NO('SW1')]]*5)]:
            with self.assertRaises(PLCError):ladder(source,{'SW1':False,'SW2':False})

    def test_scan_returns_current_lamp_without_grading(self):
        result=grade({'quest':50,'mode':'run','source':'LAMP := SW1;','inputs':'{"SW1":true,"SW2":false}'})
        self.assertTrue(result['passed']);self.assertTrue(result['signals']['LAMP']);self.assertNotIn('assignment is complete',result['feedback'])

    def test_plc_reference_examples(self):
        catalog=json.loads((ROOT/'app/static/plc-helper.json').read_text(encoding='utf-8'))
        for entry in catalog['entries']:
            with self.subTest(entry=entry['name']):
                code=entry.get('program',entry['example'])
                value=ladder(code,entry['test_inputs']) if entry['engine']=='plc-ladder' else st_scan(parse_st(code),entry['test_inputs'])
                self.assertEqual(value,entry['expected_lamp'])

if __name__=='__main__':unittest.main()
