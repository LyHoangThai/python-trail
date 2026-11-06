# 38 · Bubble the marbles

**Topic:** Bubble sort · **Chapter:** 1

Compare neighboring marbles. If the left one is bigger, swap them. Repeat, and big marbles bubble toward the end. Bubble sort is easy to see but makes many comparisons on long lists.

## Your assignment

Use nested for loops to bubble-sort marbles in ascending order, swapping neighboring values when needed. Print marbles. Do not use sort() or sorted().

The matching lesson number on the website is **38**. Its saved file is **assignment.py**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Use nested loops, compare neighbors and update marbles.
- Practice the algorithm without sort() or sorted().

Expected output:

```text
[1, 2, 3]
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/38 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (Ctrl+S), then choose Tasks: Run Test Task → Trail: Turn in assignment in the Python Trail dev container. Ctrl+Shift+B only runs Python; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

For each pass, compare marbles[j] and marbles[j + 1]. Swap them with a, b = b, a.
