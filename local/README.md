# Python Trail — local edition

A local Python learning lab for one child and parent on one Windows computer. The browser teaches and shows progress; **VS Code is the playground**. All 25 quests are unlocked, including variables, lists and dictionaries. No paid API, subscription or cloud database is used.

## First setup (Windows)

1. Extract the entire download to a permanent folder you own, for example `Documents\PythonTrail`. Avoid moving it after starting the containers.
2. Open PowerShell in that folder and run:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
   ```

   This bypass applies only to this process. It does not change your machine's execution policy. Read the script before running it.

3. Setup installs Docker Desktop and VS Code through WinGet if missing, installs the Dev Containers extension, generates a local database password, downloads/builds the containers and opens the learning dashboard. It preserves existing code and progress on reruns. Prerequisite package agreements are accepted by the script; Docker Desktop may still require first-launch terms and Windows may request administrator permission. The script checks Docker Desktop’s Linux engine; it does not call WSL or configure a backend. Finish Docker Desktop’s own prerequisite/backend prompts and restart if requested, then run setup again.
4. In VS Code, open the Command Palette (`Ctrl+Shift+P`) and choose **Dev Containers: Reopen in Container**. Accept the workspace trust prompt only for your extracted copy. Allow the Python extension/server download to finish.

Internet is needed for the initial packages, images and VS Code extension downloads. The lessons, grading and dashboard need no external service once installed. No host Python, Node.js, Git or separate PostgreSQL installation is necessary. Docker Desktop's Windows and selected-backend requirements still apply; see [Docker's Windows installation guide](https://docs.docker.com/desktop/setup/install/windows-install/). This package targets Windows, not macOS/Linux installation.

If Docker/VS Code are already installed, use `setup.ps1 -SkipInstall`. It still installs the Dev Containers extension and builds containers. `-NoOpen` suppresses opening the browser/editor.

## Daily use

Start Docker Desktop, then run `start.ps1`. Visit **http://localhost:8765**.

1. Choose a quest in the learning website. It labels the topic (for example Variables, Lists or Dictionaries) and marks it as the current quest.
2. Click **Open quest in VS Code** or find the matching file inside the container's `quests/` folder. Desktop links can open a local VS Code window; if that happens, reopen `student/` in the dev container and use its Explorer.
3. Read the commented mission, edit the starter code, then **save** the file.
4. In the Command Palette choose **Tasks: Run Test Task → Trail: Check current quest**. The terminal shows worker output and feedback. The parent dashboard refreshes every 3 seconds.
5. Use **Trail: Start current quest** to update the current topic before submitting if you opened a file directly in VS Code.

For free play, open `playground.py`. **Ctrl+Shift+B** runs the current Python file; interactive `input()` works in the terminal. The normal Python Run button also runs files, but does **not** submit or award completion. Use the Check task for that. Do not run the task from the local Windows window: `/tools/trail.py` and Python are provided inside the container.

Quest grading is noninteractive and checks defined expected output and basic language techniques. Use the input-enabled playground for interactive experiments. Hints and worked solutions are available in the website. Checkers guide practice; they are not exams or proof of mastery.

## What parents see

- Last quest explicitly started or submitted and its topic.
- Per-topic completed counts, including Variables, Lists and Dictionaries.
- Attempts per quest and recent checks with timestamps/results.

The dashboard does not watch your child's keystrokes or automatically detect an edited file. Opening a quest marks it current; the Start task or Check task updates it from VS Code. Free play does not mark curriculum completion. This is a single-learner installation, with no separate parent password or remote-device sync. Anyone using the same computer can view progress. The previous hosted site's browser-local progress is separate and is not migrated automatically.

## Containers and data

```text
Browser at localhost:8765 ── app ── PostgreSQL (progress volume)
                               └─ jobs in queue volume
VS Code ── playground ── app         │
                               offline worker
```

The web app is bound to `127.0.0.1`; PostgreSQL has no published port. The worker has **no network**, no Docker socket, no student-folder mount, and no database credentials. Each submitted program runs as an unprivileged subprocess with a timeout and process/memory/output limits inside a read-only-root container. The playground mounts only student code and read-only submission tools; it can access the app but not the database network. Container limits are intended for family practice, not hostile multi-tenant code hosting. Do not expose this app publicly.

PostgreSQL stores starts, submitted source, results and completed quests in a persistent Docker volume. Student `.py` files live in `student/` on your computer. `stop.ps1` preserves both. Never run `docker compose down -v` unless you intend to erase the database and queue. Preserve `.env` with your installation; rotating its password alone will not update an existing database's password.

Run `backup.ps1` while containers are running to save a PostgreSQL custom-format dump and a ZIP of student files under `backups/`. Backups contain submitted source and learning history. To restore a dump into a fresh installation: stop submissions, copy the dump into the database container with `docker compose cp`, then run `pg_restore --username=trail --dbname=trail --clean --if-exists` against it using `docker compose exec -T db`. This replaces database contents; save a backup first. Student files are restored separately from their ZIP. Pending submissions are recovered from the DB on app restart.

## Troubleshooting

```powershell
docker compose ps
docker compose logs --tail 60 app worker db
docker compose up -d --build --wait
```

- Docker not ready: open Docker Desktop, finish its setup and select Linux containers, then rerun setup. The app works with any Docker Desktop backend capable of running these Linux containers.
- Docker requests WSL: this is a Docker Desktop backend prerequisite, not an application installer step. Docker Desktop can use Hyper-V on supported Windows editions with the all-users installation. Windows Home does not provide the full Hyper-V feature; follow Docker Desktop’s supported options for your machine. The script does not select or change your backend.
- Port 8765 in use: stop the other local app or edit Compose's host port and dashboard/API references consistently.
- Dev container Python extension download fails: check the network and rerun **Dev Containers: Rebuild Container**.
- A check remains queued: confirm the worker is running and inspect its logs. Restart the worker if needed; interrupted work is retried. Restart the app to recover any DB-persisted submissions missing a queue file.
- A file changed during a failed check: the check uses the source saved at submission time. Save again and resubmit.
- Moved folder: stop the old Compose stack, move files, rerun setup to update file links and bind mounts.

## Validation and limits

Functional checks are in `tests/test_local.py`. Run `python -m unittest discover -s tests -v` on a host with Python. They cover all reference solutions, negative grading cases, queue-to-progress integration, API validation, and source persistence using an in-memory store. Windows tests run submitted Python without the Linux resource restrictions; the production worker always enables them.

This delivery was checked without Docker installed. Docker builds, PostgreSQL integration, Linux resource enforcement, VS Code container attachment and system installation still require a real-machine smoke test. After setup, run `smoke-test.ps1`: it submits the first reference solution, polls the actual worker, and confirms its completion in PostgreSQL through the API. This records quest 1 as completed.

The implementation uses [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/create-dev-container) and [WinGet package installation](https://learn.microsoft.com/en-us/windows/package-manager/winget/install).
