FROM python:3.12

WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "12010:8000", "--reload"]
