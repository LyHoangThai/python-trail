# 41 · Stack the plates

**Topic:** Stacks · **Chapter:** 1

A stack is like a pile of plates: the last plate added is the first one removed. A Python list can be a stack. append() puts an item on top; pop() takes the top item off.

## Your assignment

Append plate to stack, pop the top plate and print it, then print the remaining stack.

The matching lesson number on the website is **41**. Its saved file is **assignment.py**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Use append() and pop() for last-in, first-out behavior.

Expected output:

```text
red
['blue']
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/41 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (Ctrl+S), then choose Tasks: Run Test Task → Trail: Turn in assignment in the Python Trail dev container. Ctrl+Shift+B only runs Python; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Use stack.append(plate), then print(stack.pop()), then print(stack).
