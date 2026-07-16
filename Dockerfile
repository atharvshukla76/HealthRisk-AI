FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn pytest httpx

COPY . .

# Expose ports for both FastAPI and Streamlit
EXPOSE 8000 8501

# Command is overridden in docker-compose
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
