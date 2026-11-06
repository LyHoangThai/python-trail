# 37 · Guess the secret shelf

**Topic:** Binary search · **Chapter:** 1

On a sorted shelf, check the middle first. If your target is smaller, keep only the left half; otherwise keep the right half. Binary search keeps cutting the job in half. It needs sorted input.

## Your assignment

Define binary_find(numbers, target) with low/high bounds, a while loop and a middle index. Return True if target is found, otherwise False. Print the result.

Edit **assignment.py** in this folder. The matching lesson number on the website is **37**.

## What this lesson checks

- Use a while loop and a middle index calculated with // inside binary_find.
- Handle targets at both ends and a missing target.

Expected output:

```text
True
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/37 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (**Ctrl+S**), then choose **Tasks: Run Test Task → Trail: Turn in assignment** in the Python Trail dev container. The task works with this README or assignment.py open. **Ctrl+Shift+B** only runs code; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Start low = 0 and high = len(numbers) - 1. While low <= high, use middle = (low + high) // 2 and move a bound past the middle.
