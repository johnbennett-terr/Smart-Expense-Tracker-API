# Smart Expense Tracker

A REST API for tracking expenses, built with FastAPI and JSON-file storage.

(Full local setup and usage instructions coming in a later step.)

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
