FROM python:3.12-slim
WORKDIR /app
COPY apps/api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY apps/api /app
COPY datasets /datasets
ENV LIFECYCLE_SEED_FILE=/datasets/lifecycle/sample_lifecycle_events.json
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
