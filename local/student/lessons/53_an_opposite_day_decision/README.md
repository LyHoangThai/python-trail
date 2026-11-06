# 53 · An opposite-day decision

**Topic:** Structured Text · **Chapter:** 2

IF checks a condition, THEN chooses the first instructions, and ELSE chooses the other instructions. END_IF; closes the choice. NOT flips a BOOL value. This looks different from Python: there is no colon, and assignments use :=.

## Your assignment

Use IF NOT SW1 THEN / ELSE / END_IF; to turn the lamp ON when SW1 is OFF and OFF when it is ON.

The matching lesson number on the website is **53**. Its saved file is **assignment.st**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Test all four combinations of SW1 and SW2.
- Use the contact or Structured Text idea described in the assignment.

Expected output:

```text
SW1 OFF → LAMP ON
SW1 ON → LAMP OFF
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/53 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Use the browser PLC simulator for interactive practice. The saved file is assignment.st. You can turn in this file with the optional VS Code task, but the Python Run command cannot execute Ladder Logic or Structured Text.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

In the THEN branch assign TRUE to LAMP. In ELSE assign FALSE.
