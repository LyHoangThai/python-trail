# 49 · The opposite-day contact

**Topic:** Ladder Logic · **Chapter:** 1

A normally closed contact —|/|— checks for FALSE. It passes when its switch is OFF. This is a program instruction checking a bit; it is not a claim about a physical switch’s wiring.

## Your assignment

Use a normally closed SW1 contact so the lamp is ON when SW1 is OFF, and OFF when SW1 is ON.

The matching lesson number on the website is **49**. Its saved file is **assignment.ladder.json**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Test all four combinations of SW1 and SW2.
- Use the contact or Structured Text idea described in the assignment.

Expected output:

```text
SW1 OFF → LAMP ON
SW1 ON → LAMP OFF
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/49 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Use the browser PLC simulator for interactive practice. The saved file is assignment.ladder.json. You can turn in this file with the optional VS Code task, but the Python Run command cannot execute Ladder Logic or Structured Text.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Select SW1, then change the contact type from normally open to normally closed.
