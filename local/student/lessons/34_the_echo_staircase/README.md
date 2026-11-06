# 34 · The echo staircase

**Topic:** Recursion · **Chapter:** 1

A recursive function calls itself to solve a smaller version of a problem. Imagine stepping down stairs: each call takes one step. The stopping rule is the ground floor—without it, you never stop.

## Your assignment

Define countdown(n). If n is greater than 0, print n and call countdown(n - 1). Call countdown(start) with start set to 3.

Edit **assignment.py** in this folder. The matching lesson number on the website is **34**.

## What this lesson checks

- Use a countdown function that calls itself.
- Stop at zero and handle other starting values.

Expected output:

```text
3
2
1
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/34 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (**Ctrl+S**), then choose **Tasks: Run Test Task → Trail: Turn in assignment** in the Python Trail dev container. The task works with this README or assignment.py open. **Ctrl+Shift+B** only runs code; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Put the recursive call inside if n > 0:. When n is 0, do nothing.
