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

## Browser workspace, lesson folders and dedicated routes

- Migrated 25 saved assignment files into student/lessons/NN_name/assignment.py, with lesson instructions and identity files. Migration tests verify saved code is preserved and reruns do not overwrite it.
- Added /learn, /lessons/ID, /playground, /parent and /parent/submissions/ID. The old combined page is removed; / redirects to /learn.
- Browser drafts persist in PostgreSQL. Run executes Python without creating a turn-in; Turn in assignment saves a source snapshot and grades it. Playground supports prepared answers for input().
- Parent history has lesson filters, pagination, full saved source, output/feedback, and a diff against the previous attempt for the same lesson. First attempts use the starter as their baseline.
- 18 functional tests passed, including all reference solutions, separate page routing, run-versus-submit behavior, input(), migration, identity validation and diff edge cases. JavaScript/Python syntax and PowerShell setup regression checks passed.
- Live browser checks: edited and ran lesson 1, saved and reloaded its draft, turned it in and saw completion, opened /parent, followed its review link and visually verified source and highlighted changes at the dedicated submission URL. Saved submission-review.png as visual evidence.
- Live API checks: folder-based VS Code turn-in worked, exact source snapshots and diffs were preserved, lesson filtering/pagination worked, old submissions remained; Run produced output without adding a turn-in. The browser playground read Pip through input() and returned Welcome, Pip!.
- Sample submissions for lesson 1 are clearly labeled as tests. A user changed the lesson draft during testing; it was left untouched. Submitted versions remain intact regardless of later draft edits.
- Increased the optional VS Code playground to 2 GB memory, 512 processes and 2 CPUs after its editor processes filled the original 512 MB limit. Worker limits are unchanged. VS Code now uses an optional Compose profile; the default stack contains only app, db and worker.
- Rebuilt and restarted the local app/worker successfully while retaining the existing database volumes. Browser layout checks included the parent diff screen. Interactive desktop VS Code task execution remains optional and is not fully UI-verified.

## Five paths, grading audit, tabs and result banners

- Expanded to 45 lessons: Beginner 25; Intermediate, Advanced, Algorithms and Data Structures 5 each. All have original short explanations, missions, hints, worked solutions, visible checklists and matching lesson folders. Prerequisite suggestions use plain language and concrete examples.
- Audited the original 25 grading rules. Learning objectives now need to contribute to output; unused filler generally does not satisfy the checks. Changed-input cases check variables, f-strings, arithmetic, control boundaries, loops, functions and dictionaries. Basic printing lessons intentionally allow direct print statements.
- Added grading requirements and input cases for the 20 new lessons, including class/generator reuse, search edge cases, sorting, queues and graph routes. Added targeted cases for f-strings without interpolation, unused f-strings, wrong boundaries and unrelated dictionary-key updates. Valid alternatives (including augmented assignments, intermediate variables and an additive doubling function) are accepted.
- 25 Python test methods passed, including all 45 reference solutions, incorrect/shortcut cases across all 45 lessons, and execution/output checks for all 46 Helper entries. Three frontend regression groups passed: home progress refresh after browser-cache navigation, correct/retry banners with accessible roles, and history tab switching without altering the editor.
- All 45 reference solutions also passed in the production Linux worker. Plain-string, fixed f-string and unused-f-string shortcuts were rejected for lesson 8 without creating student submissions.
- Browser checks verified all five path tabs, route context, Completed labels on return to All Lessons, Description/History tabs, viewing a previously submitted answer, Output/Helper tabs, category filtering, search and a method example. Lesson history scrolls independently from the editor.
- Helper has 46 local examples across strings, integers, decimals, lists, dictionaries, sets, tuples and booleans. Methods, built-ins, operators and syntax are labeled separately. Examples are original and checked against Python 3.12 behavior.
- Live banner tests submitted two explicitly labeled lesson-1 samples: one correct answer and one needing revision. Both top banners displayed the actual result; their History button opened the matching attempt. The original lesson-1 browser draft was restored and saved. Images: assignment-correct-banner.png and assignment-retry-banner.png.
- Prior submission history and completion records are preserved. New grading rules apply on new turn-ins; old results are not silently rewritten. A failed retry does not erase a previously earned completion, and the lesson status distinguishes that case. Run is labeled not graded and does not award completion.
