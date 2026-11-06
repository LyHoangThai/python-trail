# 48 · Either doorbell works

**Topic:** Ladder Logic · **Chapter:** 1

Parallel paths are like two doors into the same room: either path can let the signal through. This is OR logic.

## Your assignment

Build two parallel paths: SW1 on one, SW2 on the other. Either switch should turn on the lamp.

The matching lesson number on the website is **48**. Its saved file is **assignment.ladder.json**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Test all four combinations of SW1 and SW2.
- Use the contact or Structured Text idea described in the assignment.

Expected output:

```text
Either switch ON → LAMP ON
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/48 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Use the browser PLC simulator for interactive practice. The saved file is assignment.ladder.json. You can turn in this file with the optional VS Code task, but the Python Run command cannot execute Ladder Logic or Structured Text.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Drag the contacts to separate new parallel paths. Connect the LAMP coil.
