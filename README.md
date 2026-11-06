# Python Trail

This folder is the main project location for future work. It brings together the original hosted website, the local Docker/VS Code edition, lesson source material, and existing release archives. Earlier copies outside this folder are retained so previous download links keep working; make future changes here.

## Project layout

| Folder | Contents |
| --- | --- |
| `local/` | Main local application: dashboard/API, PostgreSQL configuration, offline grading worker, VS Code playground, 25 quests, setup scripts and tests |
| `hosted/` | Original browser-based website with 20 quests; Site identity retained in `.openai/hosting.json` |
| `curriculum/` | Original lesson data used to generate the local edition |
| `tools/` | Curriculum generation helper, with paths relative to this project |
| `releases/` | Previously delivered ZIPs and original hosted deployment archive; snapshots, not live source |

## Run the local edition

Open PowerShell in `local/`, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
```

Follow [the local setup guide](local/README.md) for prerequisites, the VS Code workflow, backups and troubleshooting. The website runs at http://localhost:8765. Choose **Dev Containers: Reopen in Container** in VS Code to use the Python playground and grading tasks.

## Development and status

- The local edition is the main direction: real VS Code files, containerized worker, persistent PostgreSQL progress, and a parent dashboard.
- Local curriculum includes variables, arithmetic, f-strings, conditions, boolean logic, loops, lists, functions and dictionaries.
- Functional tests passed before consolidation, including all 25 reference solutions, failed checks, timeouts, queue recovery and progress updates. The source copies were verified byte-for-byte during consolidation.
- Live Docker checks passed on 2026-11-06: container builds/startup, PostgreSQL persistence, production-worker grading for all 25 solutions, worker uid/queue isolation, infinite-loop termination, the playground submission CLI and browser dashboard. Interactive VS Code attachment is the remaining manual check. See [testing results](TESTING.md).
- The hosted website is [Python Trail](https://python-trail-lab.roantortoise1.chatgpt.site). Its browser-local progress is separate from the local edition. Organizing files does not redeploy it.

Run functional tests from `local/`:

```powershell
python -m unittest discover -s tests -v
```

`tools/prepare_local.py` regenerates lesson metadata and creates missing starter files. It preserves existing student quest files. It also refreshes the local base stylesheet from the hosted version. Edit or run it deliberately; the local lesson JSON currently contains the complete 25-quest curriculum.

Generated caches, local database credentials (`.env`), and backups are excluded from Git. PostgreSQL data remains in Docker's persistent volume, not in this source folder. Do not commit a student's personal data or local secrets.
