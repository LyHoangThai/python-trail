# 40 · Shortest path to the park

**Topic:** Breadth-first search · **Chapter:** 1

Imagine a map of paths between places. Breadth-first search checks places one step away, then two steps away. A queue keeps that order. On this unweighted map, the first time you reach the park gives the fewest steps.

## Your assignment

Use a deque queue of (place, steps), a visited set and a while loop to find the shortest route from start to goal. Print the step count, or -1 if there is no route.

The matching lesson number on the website is **40**. Its saved file is **assignment.py**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Explore a graph using a queue, popleft() and a visited set.
- Return the shortest number of steps or -1 when unreachable.

Expected output:

```text
2
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/40 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (Ctrl+S), then choose Tasks: Run Test Task → Trail: Turn in assignment in the Python Trail dev container. Ctrl+Shift+B only runs Python; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Begin with queue = deque([(start, 0)]). Pop from the left, check the goal, then add unvisited neighbors with one more step.
