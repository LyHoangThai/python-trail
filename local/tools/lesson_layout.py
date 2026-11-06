"""Create one student folder per lesson without replacing student code."""
import html
import json
from pathlib import Path
import re

def lesson_folder(lesson):
    return Path(lesson['filename']).stem

def create_lesson(lesson, student_root):
    student_root=Path(student_root).resolve()
    folder=(student_root/'lessons'/lesson_folder(lesson)).resolve()
    if not folder.is_relative_to(student_root): raise ValueError('Lesson folder escapes student workspace')
    folder.mkdir(parents=True,exist_ok=True)
    engine=lesson.get('engine','python')
    assignment_name='assignment.ladder.json' if engine=='plc-ladder' else 'assignment.st' if engine=='plc-st' else 'assignment.py'
    assignment=folder/assignment_name
    legacy=(student_root/'quests'/lesson['filename']).resolve()
    if not legacy.is_relative_to(student_root): raise ValueError('Legacy path escapes student workspace')
    if legacy.exists():
        # Move the saved file byte-for-byte, including any work already done.
        if assignment.exists():
            if legacy.read_bytes()!=assignment.read_bytes():
                raise ValueError(f'Two different saved assignments exist: {legacy} and {assignment}. Resolve them before regenerating.')
        else: legacy.rename(assignment)
    if not assignment.exists():
        header=f"# Lesson {lesson['id']:02d}: {lesson['title']}\n# Read README.md, then edit this file.\n# Save and run: Trail: Turn in assignment\n\n" if engine=='python' else ''
        assignment.write_text(header+lesson['starter']+'\n',encoding='utf-8')
    # Only update old task wording in the generated comment; never edit student code.
    data=assignment.read_bytes()
    updated=data.replace(b'# Save, then Tasks: Run Test Task (Trail: Check current quest).',b'# Save, then Tasks: Run Test Task (Trail: Turn in assignment).')
    if updated!=data: assignment.write_bytes(updated)
    manifest={'id':lesson['id'],'title':lesson['title'],'topic':lesson['topic'],'assignment':assignment_name}
    (folder/'lesson.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    explanation=html.unescape(re.sub(r'<[^>]+>','',lesson['explain'].replace('<code>','`').replace('</code>','`')))
    file_workflow=(f'Use the browser PLC simulator for interactive practice. The saved file is {assignment_name}. You can turn in this file with the optional VS Code task, but the Python Run command cannot execute Ladder Logic or Structured Text.' if engine.startswith('plc-') else 'Edit assignment.py in this folder, save (Ctrl+S), then choose Tasks: Run Test Task → Trail: Turn in assignment in the Python Trail dev container. Ctrl+Shift+B only runs Python; it does not turn it in.')
    instructions=f"""# {lesson['id']:02d} · {lesson['title']}

**Topic:** {lesson['topic']} · **Chapter:** {lesson['chapter']}

{explanation}

## Your assignment

{lesson['mission']}

The matching lesson number on the website is **{lesson['id']:02d}**. Its saved file is **{assignment_name}**. Use the browser simulator for PLC exercises.

## What this lesson checks

{chr(10).join('- '+item for item in lesson.get('checks', []))}

Expected output:

```text
{lesson['expected']}
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/{lesson['id']} for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

{file_workflow}

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

{lesson['hint']}
"""
    (folder/'README.md').write_text(instructions,encoding='utf-8')
    lesson['directory']='lessons/'+folder.name
    lesson['assignment_path']=lesson['directory']+'/'+assignment_name
    return assignment
