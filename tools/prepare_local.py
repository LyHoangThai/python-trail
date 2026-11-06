import json,re
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(PROJECT/'local/tools'))
from lesson_layout import create_lesson
sys.path.insert(0,str(PROJECT/'local/worker'))
from rubric import CHECKS
from new_lessons import LESSONS as EXTRA_LESSONS
from plc import PLC_LESSONS
root=PROJECT/'local'
original=json.loads((PROJECT/'curriculum/original-lessons.json').read_text(encoding='utf-8'))
topics=['Printing','Printing','Arithmetic','Comments','Printing','Variables','Variables','F-strings','Arithmetic','Variables','Conditions','Conditions','Conditions','Boolean logic','Conditions','Loops','Loops','Lists','Functions','Functions']
lessons=[]
for i,l in enumerate(original,1):
 slug=re.sub(r'[^a-z0-9]+','_',l[0].lower()).strip('_')
 filename=f'{i:02d}_{slug}.py'
 lessons.append(dict(id=i,title=l[0],topic=topics[i-1],chapter=(i-1)//5+1,explain=l[2],mission=l[4],hint=l[5],starter=l[3],solution=l[6],expected=l[7],filename=filename))
extras=[
 ('A character dictionary','A dictionary stores values under keys. For example, hero = {"name": "Pip"}. Use hero["name"] to read a value.','Create hero with name Pip and level 1. Print the name, then the level on separate lines.','Use hero = {"name": "Pip", "level": 1}.','hero = {}\n# Read the name and level\n','hero = {"name": "Pip", "level": 1}\nprint(hero["name"])\nprint(hero["level"])','Pip\n1'),
 ('Level up','Change a dictionary value by assigning to a key: hero["level"] = 2.','Start with a hero dictionary containing level 1. Update level to 2 and print it.','Read the old level and add 1.','hero = {"name": "Pip", "level": 1}\n','hero = {"name": "Pip", "level": 1}\nhero["level"] += 1\nprint(hero["level"])','2'),
 ('A missing key','dictionary.get(key, default) returns a fallback when a key does not exist. This helps avoid KeyError.','Create a hero dictionary without a pet key. Use get() to print No pet yet as a default.','Try hero.get("pet", "No pet yet").','hero = {"name": "Pip"}\n','hero = {"name": "Pip"}\nprint(hero.get("pet", "No pet yet"))','No pet yet'),
 ('Inventory report','Loop through dictionary.items() to get each key and value together: for item, count in bag.items():.','Loop through bag and print map: 1, then snack: 3, each on its own line.','Use print(f"{item}: {count}") inside the loop.','bag = {"map": 1, "snack": 3}\n','bag = {"map": 1, "snack": 3}\nfor item, count in bag.items():\n    print(f"{item}: {count}")','map: 1\nsnack: 3'),
 ('Your explorer registry','A list can contain dictionaries. A function can accept a dictionary as its parameter. Combine these tools for a little registry.','Define introduce(hero). Loop through heroes and call introduce to print Pip is level 1, then Nova is level 2.','In introduce use print(f"{hero[\'name\']} is level {hero[\'level\']}").','heroes = [{"name": "Pip", "level": 1}, {"name": "Nova", "level": 2}]\n\ndef introduce(hero):\n    pass\n\n# Introduce each hero\n','heroes = [{"name": "Pip", "level": 1}, {"name": "Nova", "level": 2}]\n\ndef introduce(hero):\n    print(f"{hero[\'name\']} is level {hero[\'level\']}")\n\nfor hero in heroes:\n    introduce(hero)','Pip is level 1\nNova is level 2')]
for i,e in enumerate(extras,21):
 title,explain,mission,hint,starter,solution,expected=e
 filename=f'{i:02d}_'+re.sub('[^a-z0-9]+','_',title.lower()).strip('_')+'.py'
 lessons.append(dict(id=i,title=title,topic='Dictionaries',chapter=5,explain=explain,mission=mission,hint=hint,starter=starter,solution=solution,expected=expected,filename=filename))
for lesson in lessons:
 lesson['track']='beginner'
 lesson['checks']=CHECKS[lesson['id']]
 if lesson['id']==15: lesson['mission']=lesson['mission'].replace('We check three scores.', 'We also check scores at the 50 and 80 boundaries.')
 if lesson['id']==24: lesson['mission']='Use bag.items() in a for loop and print map: 1, then snack: 3, each on its own line.'
 create_lesson(lesson,root/'student')
for extra in EXTRA_LESSONS+PLC_LESSONS:
 lesson=dict(extra)
 slug=re.sub(r'[^a-z0-9]+','_',lesson['title'].lower()).strip('_')
 lesson['filename']=f"{lesson['id']:02d}_{slug}.py"
 create_lesson(lesson,root/'student')
 lessons.append(lesson)
(root/'app/lessons.json').write_text(json.dumps(lessons,ensure_ascii=False,indent=2),encoding='utf-8')
index=['# Lessons','', 'One folder per lesson. Read its README.md and use the matching browser lesson. Python files and optional PLC source files can also be turned in with the VS Code task.', '', '| Lesson | Topic |','| --- | --- |']
for lesson in lessons:
 index.append(f"| [{lesson['id']:02d} · {lesson['title']}]({Path(lesson['directory']).name}/README.md) | {lesson['track']} · {lesson['topic']} |")
(root/'student/lessons/README.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
legacy=root/'student/quests'
if legacy.exists() and not any(legacy.iterdir()): legacy.rmdir()
(root/'app/static').mkdir(exist_ok=True)
(root/'app/static/style.css').write_text((PROJECT/'hosted/dist/style.css').read_text(encoding='utf-8').replace("'Space Grotesk'","'Segoe UI'").replace("'DM Sans'","'Segoe UI'").replace("@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');",''),encoding='utf-8')
print(f'Generated {len(lessons)} lessons and local assets.')
