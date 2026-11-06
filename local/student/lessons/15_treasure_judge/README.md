# 15 · Treasure judge

**Topic:** Conditions · **Chapter:** 3

Write a reward system. Check the biggest reward first so a score of 90 does not get the lower reward.

## Your assignment

Use if / elif / else to print Gold for 80+, Silver for 50–79, and Bronze otherwise. We also check scores at the 50 and 80 boundaries.

Edit **assignment.py** in this folder. The matching lesson number on the website is **15**.

## What this lesson checks

- Use if / elif / else for Gold, Silver and Bronze.
- Check boundaries at 50 and 80 as well as other scores.

Expected output:

```text
Gold
```

## Learn and turn in through the browser

Open http://localhost:8765/lessons/15 for this lesson's instructions, code editor and output on one screen. Your browser draft saves automatically on this computer.

1. Write code in the browser editor.
2. Click **Run code** to try it. Running does not create a submission.
3. Click **Turn in assignment** when ready. It saves the code version, checks it, and gives you a submission ID.
4. If it needs revision, edit and turn it in again. Every attempt is saved.

Parents can review the history at http://localhost:8765/parent and open any attempt to see its source, result, output and changes from the previous attempt.

## Optional VS Code workflow

Edit assignment.py in this folder, save (**Ctrl+S**), then choose **Tasks: Run Test Task → Trail: Turn in assignment** in the Python Trail dev container. The task works with this README or assignment.py open. **Ctrl+Shift+B** only runs code; it does not turn it in.

Browser drafts and optional assignment.py files are separate workspaces. Both submit to the same lesson history; neither overwrites the other's draft.

## Hint

Start with if score >= 80:, then elif score >= 50:.
