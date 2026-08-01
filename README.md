# Smart Expense Tracker

A REST API for tracking expenses, built with FastAPI and JSON-file storage
(no database required).

## Requirements

- Python 3.10+ available on your machine.

## Setup

Clone the repo and `cd` into it, then follow the commands for your platform.

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If `python` isn't recognized (a common issue on Windows when the Microsoft
Store's app-execution alias intercepts it instead of a real install), use the
`py` launcher instead:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If activation fails with a message about running scripts being disabled, your
PowerShell execution policy is blocking it. Allow local scripts for your user
(one-time fix) and re-run activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### macOS / Linux (bash/zsh)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the server

With the virtual environment activated:

```
uvicorn src.main:app --reload
```

The API is now available at `http://localhost:8000`. Interactive API docs
(Swagger UI) are at `http://localhost:8000/docs`.

Expense data is stored in `expenses.json` in the project root and persists
across server restarts.

## Running the tests

With the virtual environment activated:

```
pytest
```

Each test run uses its own temporary, isolated data file, so tests never
touch `expenses.json` or affect each other's state.

## Running with Docker

Build the image from the project root:

```
docker build -t smart-expense-tracker .
```

Run it, mapping the API's port and mounting a local folder so expense data
persists across container restarts and image rebuilds (data is **not**
baked into the image — it lives only in the mounted folder):

**PowerShell:**
```powershell
docker run -d --name expense-tracker -p 8000:8000 -v "${PWD}\data:/data" smart-expense-tracker
```

**bash / macOS / Linux:**
```bash
docker run -d --name expense-tracker -p 8000:8000 -v "$(pwd)/data:/data" smart-expense-tracker
```

This creates a `data/` folder next to the Dockerfile containing
`expenses.json`. The API is then reachable at `http://localhost:8000`.

To use a different port, override both the host mapping and the `PORT`
environment variable together, e.g. to run on 9000:

```powershell
docker run -d --name expense-tracker -p 9000:9000 -e PORT=9000 -v "${PWD}\data:/data" smart-expense-tracker
```

To stop and remove the container:

```
docker rm -f expense-tracker
```

## API overview

| Method | Path                        | Description                                    |
|--------|-----------------------------|-------------------------------------------------|
| POST   | `/expenses`                 | Create an expense (201)                        |
| GET    | `/expenses`                 | List expenses, optional `?category=` filter    |
| GET    | `/expenses/{id}`            | Fetch one expense (404 if missing)             |
| DELETE | `/expenses/{id}`            | Delete an expense (204, 404 if missing)        |
| GET    | `/expenses/total`           | Total amount, optional `?category=` filter     |
