# 28 · Tidy the name tag

**Topic:** String methods · **Chapter:** 1

A name tag can arrive with messy spaces and lowercase letters. `text.strip()` trims its edges, and `text.title()` gives words capital initials. Each method returns new text; it does not change the old string.

## Your assignment

Use strip() and title() on label, then print the tidy name tag: Captain Nova.

The matching lesson number on the website is **28**. Its saved file is **assignment.py**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Use both strip() and title() in the text you print.
- Work with the label variable.

Expected output:

```text
Captain Nova
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/28 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (Ctrl+S), then choose Tasks: Run Test Task → Trail: Turn in assignment in the Python Trail dev container. Ctrl+Shift+B only runs Python; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Try label.strip().title(), then print the result.
