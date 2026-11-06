"""All-lesson regression cases for meaningful use of the taught technique."""
import json
from pathlib import Path
import sys
import unittest
import contextlib
import io
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'worker'))
from worker import grade
LESSONS={q['id']:q for q in json.loads((ROOT/'app/lessons.json').read_text(encoding='utf-8'))}

class RubricAudit(unittest.TestCase):
    def check(self,quest,source):
        return grade({'quest':quest,'source':source,'expected':LESSONS[quest]['expected']},sandbox=False)

    def test_every_lesson_rejects_an_incorrect_or_shortcut_answer(self):
        wrong={
          1:'"Hello, explorer!"',2:'print("Let\'s explore!")\nprint("My name is Python")',
          3:'unused = 7 * 8\nprint(56)',4:'marker = "#"\nprint("Ready for adventure!")',5:'print(3)\nprint(2)\nprint(1)',
          6:'name = "Pip"\nprint("Pip")',7:'coins = 10\ncoins += 5\nprint(15)',
          8:'name = "Pip"\nprint(f"Hello, Pip!")',
          9:'snacks=17\nfriends=4\nunused=snacks//friends\nother=snacks%friends\nprint(4)\nprint(1)',
          10:'name="Pip"\nlevel=1\nprint("Explorer: Pip\\nLevel: 1")',
          11:'coins=12\nif True:\n    print("Gate open!")',
          12:'raining=False\nif raining:\n    pass\nprint("Bring a hat")',
          13:'door=2\nif door==2:\n    print("A treasure chest")',
          14:'has_map=True\nhas_key=True\nif has_map or has_key:\n    print("Adventure unlocked!")',
          15:'score=85\nif score>80:\n    print("Gold")\nelif score>=50:\n    print("Silver")\nelse:\n    print("Bronze")',
          16:'for turn in range(3):\n    pass\nprint("Hello!\\nHello!\\nHello!")',
          17:'for step in range(1,6):\n    pass\nprint("1\\n2\\n3\\n4\\n5")',
          18:'backpack=["map","snack","torch"]\nfor item in ["map","snack","torch"]:\n    print(item)',
          19:'def cheer():\n    print("You can do this!")\nif False:\n    cheer()\nprint("You can do this!\\nYou can do this!")',
          20:'explorers=["Pip","Nova","Ash"]\ndef welcome(name):\n    print(f"Welcome, {name}!")\nfor name in explorers:\n    print(f"Welcome, {name}!")',
          21:'hero={"name":"Pip","level":1}\nprint("Pip")\nprint(1)',
          22:'hero={"name":"Pip","level":2}\nprint(hero["level"])',
          23:'hero={"name":"Pip"}\nunused=hero.get("pet","No pet yet")\nprint("No pet yet")',
          24:'bag={"map":1,"snack":3}\nfor item,count in bag.items():\n    pass\nprint("map: 1\\nsnack: 3")',
          25:'heroes=[{"name":"Pip","level":1},{"name":"Nova","level":2}]\ndef introduce(hero):\n    print(f"{hero[\'name\']} is level {hero[\'level\']}")\nprint("Pip is level 1\\nNova is level 2")'}
        for quest,source in wrong.items():
            with self.subTest(quest=quest):self.assertFalse(self.check(quest,source)['passed'],source)

    def test_f_string_must_insert_name_and_contribute_to_output(self):
        for source in ['name="Pip"\nprint("Hello, Pip!")','name="Pip"\nunused=f"{name}"\nprint("Hello, "+name+"!")','name="Pip"\nprint(f"Hello, {\'Pip\'}!")']:
            with self.subTest(source=source):self.assertFalse(self.check(8,source)['passed'])

    def test_valid_alternatives_are_accepted(self):
        alternatives={
          3:'a=7\nb=8\nanswer=a*b\nprint(answer)',
          7:'coins=10\ncoins+=5\nprint(coins)',
          8:'name="Pip"\ngreeting=f"Hello, {name}!"\nprint(greeting)',
          9:'snacks=17\nfriends=4\nshares=snacks//friends\nleft=snacks%friends\nprint(shares)\nprint(left)',
          16:'for unused in ["a","b","c"]:\n    print("Hello!")',
          17:'for value in [1,2,3,4,5]:\n    print(value)',
          19:'def cheer():\n    print("You can do this!")\nfor turn in range(2):\n    cheer()',
          22:'hero=dict(name="Pip",level=1)\nhero.update(level=2)\nprint(hero.get("level"))'}
        alternatives[26]='number=6\ndef double(value):\n    return value + value\nprint(double(number))'
        for quest,source in alternatives.items():
            with self.subTest(quest=quest):self.assertTrue(self.check(quest,source)['passed'],self.check(quest,source))

    def test_new_tracks_reject_printed_answer_shortcuts(self):
        for quest,lesson in LESSONS.items():
            if quest<=25:continue
            with self.subTest(quest=quest):
                self.assertFalse(self.check(quest,'print('+repr(lesson['expected'])+')')['passed'])

    def test_tracks_and_lesson_identity_are_complete(self):
        tracks=['beginner','intermediate','advanced','algorithms','data-structures','plc']
        self.assertEqual(set(q['track'] for q in LESSONS.values()),set(tracks))
        self.assertEqual(len(LESSONS),53)
        self.assertEqual(len([q for q in LESSONS.values() if q['track']=='beginner']),25)
        for track in tracks[1:]:self.assertEqual(len([q for q in LESSONS.values() if q['track']==track]),8 if track=='plc' else 5)
        for lesson in LESSONS.values():self.assertTrue(lesson['checks'])

    def test_every_helper_example_runs_as_shown(self):
        catalog=json.loads((ROOT/'app/static/helper.json').read_text(encoding='utf-8'))
        self.assertEqual(set(e['category'] for e in catalog['entries']),{'str','int','float','list','dict','set','tuple','bool'})
        for entry in catalog['entries']:
            with self.subTest(example=entry['name']):
                out=io.StringIO()
                with contextlib.redirect_stdout(out):exec(entry['example'],{})
                self.assertEqual(out.getvalue().strip(),entry['output'].strip())

    def test_updating_an_unrelated_dictionary_key_does_not_count(self):
        source='hero={"level":1}\nhero["color"]=2\nprint(hero["level"]+1)'
        self.assertFalse(self.check(22,source)['passed'])

if __name__=='__main__':unittest.main()
