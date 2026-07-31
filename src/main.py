from fastapi import FastAPI

app = FastAPI(title="Smart Expense Tracker")


@app.get("/")
def root():
    return {"status": "ok"}
