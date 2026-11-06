# 32 · A friendly safety net

**Topic:** Exceptions · **Chapter:** 1

Sometimes a program gets an unexpected value. `try` attempts a job; `except ValueError` catches a number-conversion problem. A safety net helps the program explain what happened.

## Your assignment

Try converting text to an integer and print it. If conversion raises ValueError, print Please use digits. Start with text set to seven.

The matching lesson number on the website is **32**. Its saved file is **assignment.py**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Use try / except for the conversion.
- Handle both numeric text and invalid text.

Expected output:

```text
Please use digits
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/32 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (Ctrl+S), then choose Tasks: Run Test Task → Trail: Turn in assignment in the Python Trail dev container. Ctrl+Shift+B only runs Python; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Put int(text) in try, then catch ValueError and print the friendly message.
