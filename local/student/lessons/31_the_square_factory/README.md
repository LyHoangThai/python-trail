# 31 · The square factory

**Topic:** Comprehensions · **Chapter:** 1

A list comprehension is a compact factory: take each item, transform it, and collect the results. `[x * 2 for x in numbers]` makes a new list without changing numbers.

## Your assignment

Use a list comprehension to square every item in numbers. Print the new list.

Edit **assignment.py** in this folder. The matching lesson number on the website is **31**.

## What this lesson checks

- Build the printed list with a list comprehension.
- Square the actual input values.

Expected output:

```text
[1, 4, 9, 16]
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/31 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (**Ctrl+S**), then choose **Tasks: Run Test Task → Trail: Turn in assignment** in the Python Trail dev container. The task works with this README or assignment.py open. **Ctrl+Shift+B** only runs code; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

A square is a number multiplied by itself: [n * n for n in numbers].
