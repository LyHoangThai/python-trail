# Python Trail — Python & PLC Sample

**Version 0.1.1 · Local learning lab · Windows + Docker Desktop**

A working sample product for families: kids learn Python and PLC logic, submit assignments, and let parents review their progress and every revision. All 53 lessons are included. No paid learning subscription or API key is required.

## Start here

1. Extract the ZIP fully into a folder you can keep. Do not run scripts inside the ZIP.
2. Double-click **START HERE.cmd**.
3. In the window that opens, click **Set up & open Python Trail**. Progress appears in the window; your browser opens when the app is ready.

No terminal commands are needed. Use the same shortcut next time. Windows may hide the `.cmd` extension and show it as **START HERE**. If Windows blocks the downloaded launcher, review its publisher/source and Windows prompt before choosing whether to run it. Installer approvals, Docker's initial prompts, and any required restart still need your action. After a restart, open START HERE again.

For troubleshooting or automation, the PowerShell launcher is still available:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Launch-Sample.ps1
```

The launcher installs Docker Desktop if it is missing, builds the local services, creates a new local database password, and opens **http://localhost:8766/learn**. First setup needs internet and may require administrator approval or a Windows restart. Finish Docker Desktop's first-launch prompts and ensure its Linux engine is running, then rerun the launcher if needed. Docker's selected Linux backend must be available; the script does not install/configure WSL. See [the setup guide](local/README.md) for troubleshooting.

If Docker is already installed and ready, use `Launch-Sample.ps1 -SkipInstall`. For later visits use `Start-Sample.ps1`. Stop safely with `Stop-Sample.ps1`; saved work remains.

This sample uses port **8766** and Docker project **python-trail-sample**. It can run alongside the original development app on port 8765 and has separate database/queue volumes. Do not run multiple copies of this sample simultaneously; they share that sample project name. If port 8766 is occupied, stop the other sample before launching.

## What to try

- **Python:** 45 lessons across Beginner, Intermediate, Advanced, Algorithms and Data Structures; in-browser editor and searchable Helper.
- **PLC:** 4 drag-and-drop Ladder Logic lessons plus 4 Structured Text lessons; live switches, lamp, operator panel and a worker that checks every input combination.
- **Parent review:** topic progress, submitted answers, feedback, timestamps and differences between attempts.

| Open | Purpose |
| --- | --- |
| http://localhost:8766/learn | Select Python or PLC and choose a lesson |
| http://localhost:8766/lessons/46 | Start the visual ladder lesson |
| http://localhost:8766/parent | Review progress and saved submissions |
| http://localhost:8766/playground | Free Python experiments |

Follow [the 5-minute demo](DEMO.md). Open [Product-Overview.html](Product-Overview.html) for a presentation page with a screenshot.

## Included

`local/` contains the complete runnable application, setup/start/stop/backup scripts, 53 matching lesson folders, optional VS Code configuration, and tests. Every assignment file starts from the curriculum starter. This archive contains no student submissions, personal drafts, database volume, backups, `.env` file or API credentials. Those are created locally as you use it. `manifest.json` lists the shipped files and SHA-256 hashes; run `Verify-Package.ps1` before first setup to check them. The ZIP also has a separate `.sha256` file.

## Sample scope

This is a functioning prototype for local family evaluation. Student and parent screens are separate routes without authentication. The worker runs offline with execution limits; this is not a hosted classroom or public code-execution service. PLC supports one Boolean output rung with SW1/SW2 and LAMP; timers, counters, real hardware and full industrial PLC syntax are not implemented. C++ is future work. Completion records successful lesson checks, not proof of mastery.

Keep your generated `local/.env` and backups private. Use `local/backup.ps1` to back up browser drafts, history and files. Avoid `docker compose down -v`, which erases progress. Share the original ZIP, not your used installation folder. More details: [release notes](RELEASE-NOTES.md), [PLC guide](PLC.md), [grading](GRADING.md).
