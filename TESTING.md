# Live test results — 2026-11-06

Environment: Windows, Docker Desktop 4.98.0, Docker Engine 29.9.2 (`linux/amd64`), Docker Compose v5.6.1.

## Passed

- Setup generated the ignored local `.env` and installed the official VS Code Dev Containers extension.
- App, PostgreSQL, worker and playground images built; all four containers are running. App/database health checks passed.
- `local/smoke-test.ps1`: submission → worker execution → PostgreSQL completion → parent-dashboard API.
- All 25 reference solutions passed using the production Linux worker with its resource restrictions enabled. These direct worker checks did not complete the rest of the curriculum in the database.
- Student code executed with uid 65534 and received PermissionError when attempting to write `/queue/test`.
- An infinite loop was terminated by production resource limits.
- `/tools/trail.py check` executed as the playground's non-root user, submitted a temporary quest-1 file, and returned successful live worker feedback.
- The browser at http://localhost:8765 showed Local services connected, Currently learning: Printing, and quest 1 completed with two submissions. Topic cards include Variables, Lists and Dictionaries.

Two test submissions completed quest 1. The student's real starter files were not edited. Docker volumes and containers are retained for use.

## Still to verify manually

Open `local/student` in desktop VS Code. Run **Dev Containers: Reopen in Container**, wait for the Python extension/server to initialize, then save a quest and use **Tasks: Run Test Task → Trail: Check current quest**. The underlying submission CLI is tested; interactive editor attachment is not yet verified.

The setup encountered a transient container-name conflict while another startup apparently created the same stack. Inspection immediately afterward confirmed all services were healthy, so tests continued against that stack. No containers or database volumes were deleted to resolve the conflict. Avoid running two copies of setup simultaneously.
