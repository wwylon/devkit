# web.bat — standard way to start a project's web interface

Applies to every project that has a web UI (arena server, dashboard, dev server). Projects without
one (libraries, engines, tools) need no `web.bat`. Not imported by any `CLAUDE.md`; a project adopts
it by following the contract and keeping its port in the registry.

## Contract

`.\web.bat` in the repo root, run from anywhere (`cd /d "%~dp0"` first).

1. `web.bat --help` (also `-h`, `/?`) prints usage and the default URL, then exits 0.
2. Default port is **hard-coded in the file** and equals the project's line in `<portfolio-root>\ports.yaml`.
   Do not read the registry at run time (the relative depth changes when a project moves).
3. `web.bat --port N` overrides the port; extra arguments pass through to the server.
4. Binds `127.0.0.1` only.
5. Checks prerequisites first and says what to run when one is missing (build the server exe,
   `npm install`, `uv sync`, ...), exit 1.
6. Refuses to start when the port is taken, with the owner of the port in the message:
   `netstat -ano | findstr ":%PORT% " | findstr LISTENING` → print it, exit 1.
7. Starts the server, waits until it answers, then opens the browser at the URL (`start "" http://127.0.0.1:%PORT%/`).
8. Prints the URL it serves on one line, so a log shows the port.

Skeleton (Windows batch):

```bat
@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "PORT=7466"
if /i "%~1"=="--help" goto :help
if /i "%~1"=="-h" goto :help
if /i "%~1"=="--port" (set "PORT=%~2" & shift & shift)
netstat -ano | findstr ":%PORT% " | findstr LISTENING >nul && (
  echo Port %PORT% is already in use: & netstat -ano | findstr ":%PORT% " | findstr LISTENING & exit /b 1)
rem ... prerequisite checks, then start the server on 127.0.0.1:%PORT% ...
echo Serving on http://127.0.0.1:%PORT%/
start "" "http://127.0.0.1:%PORT%/"
exit /b 0
:help
echo web.bat [--port N]  - start the web UI on http://127.0.0.1:%PORT%/ (default %PORT%)
exit /b 0
```

## Ports

The registry is `<portfolio-root>\ports.yaml`, one line per port (a project with two servers has two lines).

- New port: `python devkit/tools/ports.py free` (default range 7400-7499), add the line, then use it.
- Check: `python devkit/tools/ports.py check` reports duplicates, a registered `in_use` port that
  its source file no longer mentions, and `web.bat` ports that are not registered. Run it after
  changing a port, and before adding a project.
- Two clones of one project each get their own port so both can run at once.
