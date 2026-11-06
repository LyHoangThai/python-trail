# 26 · The doubling machine

**Topic:** Return values · **Chapter:** 1

Imagine a little machine: a number goes in, and its double comes out. `return` sends a value back to the code that called your function. Printing shows a value; returning lets other code use it.

## Your assignment

Define double(number) to return twice its number. Print double(number) with number set to 6.

The matching lesson number on the website is **26**. Its saved file is **assignment.py**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Define and call double(number).
- Return a calculated value; it must work for other numbers too.

Expected output:

```text
12
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/26 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (Ctrl+S), then choose Tasks: Run Test Task → Trail: Turn in assignment in the Python Trail dev container. Ctrl+Shift+B only runs Python; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Inside double, return number * 2. Outside, print(double(number)).
