# 43 · Collect unique colors

**Topic:** Sets · **Chapter:** 1

A set is a collection of unique items, like stickers without duplicates. set(colors) removes repeated values. Sets have no display order, so use sorted() when you want a predictable list to show.

## Your assignment

Make unique = set(colors). Print its size with len(), then print sorted(unique).

The matching lesson number on the website is **43**. Its saved file is **assignment.py**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Use set() to collect unique values.
- Count and display the actual unique items.

Expected output:

```text
2
['blue', 'red']
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/43 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (Ctrl+S), then choose Tasks: Run Test Task → Trail: Turn in assignment in the Python Trail dev container. Ctrl+Shift+B only runs Python; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Use len(unique) for the count and sorted(unique) for a stable display.
