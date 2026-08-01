FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

# Data file lives outside /app so it can be volume-mounted and survives
# both container restarts and image rebuilds.
ENV EXPENSE_DATA_FILE=/data/expenses.json
VOLUME ["/data"]

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]
