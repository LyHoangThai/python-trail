# 42 · Wait your turn

**Topic:** Queues · **Chapter:** 1

A queue is a waiting line: the first person in is served first. collections.deque is a handy Python queue. append() joins the back; popleft() serves the front.

## Your assignment

Create queue = deque(people), append newcomer, then print each person as you serve the queue with popleft() in a while loop.

The matching lesson number on the website is **42**. Its saved file is **assignment.py**. Use the browser simulator for PLC exercises.

## What this lesson checks

- Build a deque and use append() and popleft().
- Serve people in first-in, first-out order.

Expected output:

```text
Ari
Bo
Cy
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/42 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (Ctrl+S), then choose Tasks: Run Test Task → Trail: Turn in assignment in the Python Trail dev container. Ctrl+Shift+B only runs Python; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Import deque from collections. While queue is not empty, print(queue.popleft()).
