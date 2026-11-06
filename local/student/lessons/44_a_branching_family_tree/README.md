# 44 · A branching family tree

**Topic:** Trees · **Chapter:** 1

A tree branches from a root into children. This tiny tree uses dictionaries: each node has a name and a children list. A for loop can visit the root’s immediate children.

## Your assignment

Print tree["name"], then loop through tree["children"] and print each child’s name.

Edit **assignment.py** in this folder. The matching lesson number on the website is **44**.

## What this lesson checks

- Read a root node and visit its immediate children.
- Use dictionary keys and a loop.

Expected output:

```text
Oak
Leaf A
Leaf B
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/44 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (**Ctrl+S**), then choose **Tasks: Run Test Task → Trail: Turn in assignment** in the Python Trail dev container. The task works with this README or assignment.py open. **Ctrl+Shift+B** only runs code; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Use for child in tree["children"]: and print(child["name"]).
