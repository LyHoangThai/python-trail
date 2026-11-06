# 47 · Two keys for the toy box

**Topic:** Ladder Logic · **Chapter:** 1

Two contacts in series are like two keys in a row. The path is true only when both contacts pass. This is AND logic.

## Your assignment

Put normally open SW1 and SW2 contacts on the same path so the lamp turns on only when both switches are ON.

The matching lesson number on the website is **47**. Its saved file is **assignment.ladder.json**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Test all four combinations of SW1 and SW2.
- Use the contact or Structured Text idea described in the assignment.

Expected output:

```text
Only both switches ON → LAMP ON
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/47 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Use the browser PLC simulator for interactive practice. The saved file is assignment.ladder.json. You can turn in this file with the optional VS Code task, but the Python Run command cannot execute Ladder Logic or Structured Text.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Choose SW2 in the toolbox. Drag its contact to the gap after SW1. Connect the LAMP coil.
