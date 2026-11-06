# 45 · A map of friendships

**Topic:** Graphs · **Chapter:** 1

A graph stores things and their connections. In an adjacency list, each dictionary key is a person and its list contains their friends. Unlike a tree, connections can circle back.

## Your assignment

Loop through graph[person] and print each friend. Start with person Ari, whose friends are Bo and Cy.

Edit **assignment.py** in this folder. The matching lesson number on the website is **45**.

## What this lesson checks

- Read the selected person’s neighbor list and loop through it.

Expected output:

```text
Bo
Cy
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/45 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (**Ctrl+S**), then choose **Tasks: Run Test Task → Trail: Turn in assignment** in the Python Trail dev container. The task works with this README or assignment.py open. **Ctrl+Shift+B** only runs code; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Use for friend in graph[person]: print(friend).
