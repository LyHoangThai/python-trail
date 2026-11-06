# Python Trail — local edition

A free local Python learning lab with 25 lessons. The main experience runs in one browser window: lesson instructions, Python editor, output and assignment turn-in. Docker Desktop runs the worker and PostgreSQL in the background. VS Code is optional.

## Setup on Windows

Open PowerShell in this folder and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
```

Setup installs Docker Desktop if missing, generates an ignored local database password, builds the containers, and opens the student page. Finish Docker Desktop's first-launch setup and restart Windows if requested before rerunning the script. The script does not invoke or install WSL; Docker Desktop manages its selected Linux backend. Initial software/images require internet. Host Python, Node.js and PostgreSQL are not required.

On later visits, start Docker Desktop and run `start.ps1`. Use `stop.ps1` to stop the application without deleting saved work.

## Separate pages

| Address | Purpose |
| --- | --- |
| http://localhost:8765/learn | Student's learning trail |
| http://localhost:8765/lessons/1 | Lesson 1, editor, output and assignment turn-in; replace 1 with any lesson number up to 25 |
| http://localhost:8765/playground | Free coding and input experiments |
| http://localhost:8765/parent | Parent progress and submission history |
| /parent/submissions/ID | A saved turn-in, full source, feedback, output and changes |

The root URL redirects to /learn. These are separate screens within one local application. They are not separate authenticated accounts; anyone using this computer can access them.

## Student workflow

1. Choose a lesson in /learn.
2. Read the short explanation and write code in its editor.
3. Click **Run code** to see what it does. Run does not create a turn-in or mark completion.
4. Click **Turn in assignment** to save a code snapshot and check the assignment. A submission ID confirms that it is saved.
5. Read the result. If it needs revision, edit and turn it in again. All attempts are kept.

Drafts autosave to the local database and are restored when reopening a lesson. Save draft and Ctrl+S also save explicitly. Ctrl+Enter runs the code. Reset to starter asks before replacing a draft and leaves submission history intact.

In /playground, enter one answer per line under Program input when using input(). Playground runs do not complete lessons or enter parent submission history.

## Parent review

The dashboard shows the last lesson explicitly started or turned in, its topic, completion counts and every turn-in. Filter by lesson and paginate through older submissions. **Review code & changes** opens a dedicated page showing:

- Exact source submitted, submission ID, attempt number and timestamp.
- Grading result, feedback and program output.
- Previous code and submitted code side by side.
- Highlighted additions/removals against the previous attempt for that same lesson. The first attempt is compared with the lesson starter.

Failed checks and unchanged resubmissions stay in history. Completion means checks passed, not proof of mastery. The app does not watch keystrokes. Progress from the original hosted website is separate.

## Lesson folders and optional VS Code

Each website lesson maps to one folder under `student/lessons/NN_name/` containing README.md, assignment.py and lesson.json. The old flat quests folder has been migrated, preserving saved student Python code. See [the lesson index](student/lessons/README.md).

To install/start the optional VS Code environment:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1 -WithVSCode
```

Open student/ in VS Code, choose **Dev Containers: Reopen in Container**, and wait for initialization. Save assignment.py, then **Tasks: Run Test Task → Trail: Turn in assignment**. The terminal prints a saved submission ID and grading result. **Trail: Start lesson** updates the current topic. Ctrl+Shift+B only runs the file.

Browser drafts and VS Code assignment files are separate workspaces; neither silently overwrites the other. Both turn in to the same parent history. The playground container has a Compose profile named vscode, so it is optional for the browser workflow. An already-running VS Code container may stay running until closed/stopped.

## Containers and persistence

The web app binds to 127.0.0.1:8765. PostgreSQL has no published port. Its persistent Docker volume stores drafts, submissions and progress. Submitted programs run in the offline worker: no network, Docker socket, student-folder mount or database credentials. Python runs as an unprivileged subprocess with time, memory, process and output limits. This is intended for family practice, not public multi-tenant code hosting.

The optional VS Code container mounts student files and read-only submission tools, uses a non-root user, and cannot access the database network. It has a larger resource allowance for the editor; worker limits remain separate.

Keep .env with this installation and do not share it. Rerunning setup preserves the database password. Never run docker compose down -v unless you intend to erase progress. Run backup.ps1 while services are running to save a PostgreSQL dump and a ZIP of student files. Browser drafts and submission history are included in the DB dump. Backups contain student code/history; keep them private.

## Troubleshooting and verification

```powershell
docker compose ps
docker compose logs --tail 60 app worker db
docker compose up -d --build --wait
```

If the browser cannot connect, check Docker Desktop's engine first. If work stays queued, check worker logs. Pending runs and submissions recover on app restart. A saved submission ID means it is in the database even if the browser stopped polling; review history before resubmitting.

For Docker without WSL, select Docker VMM under Docker Desktop Settings > General > Virtual Machine Manager if supported. Docker currently marks it Beta. See [Docker's backend guide](https://docs.docker.com/desktop/features/vmm/) and [Windows requirements](https://docs.docker.com/desktop/setup/install/windows-install/). The app needs a supported Linux container engine.

Functional tests: `python -m unittest discover -s tests -v` on a host with Python. Setup regression checks: `powershell -NoProfile -ExecutionPolicy Bypass -File tests/setup.tests.ps1`. The live smoke test, `smoke-test.ps1`, records lesson 1 as completed.

See [the project testing record](../TESTING.md) for live Docker, browser, grading and history verification. Desktop VS Code attachment remains optional and has not been fully verified through its UI.
