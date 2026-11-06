# 39 · Count the color votes

**Topic:** Frequency counting · **Chapter:** 1

Give each color a tally. A dictionary stores a color as the key and its count as the value. Each time that color appears, add one to its tally. This is frequency counting.

## Your assignment

Build counts by looping over votes and increasing counts[color] with get(color, 0) + 1. Print the number of red votes.

Edit **assignment.py** in this folder. The matching lesson number on the website is **39**.

## What this lesson checks

- Loop over votes and maintain dictionary counts.
- Use get() for a missing count.

Expected output:

```text
2
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/39 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (**Ctrl+S**), then choose **Tasks: Run Test Task → Trail: Turn in assignment** in the Python Trail dev container. The task works with this README or assignment.py open. **Ctrl+Shift+B** only runs code; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Start counts = {}. For each color, set counts[color] = counts.get(color, 0) + 1.
