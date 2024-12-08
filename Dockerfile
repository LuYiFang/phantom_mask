FROM python:3.11-slim

WORKDIR /workspace

COPY . /workspace

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip install --no-cache-dir -r api/requirements.txt

ENV PYTHONPATH=/workspace/api

EXPOSE 8000

CMD ["sh", "-c", "cd /workspace/api && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
