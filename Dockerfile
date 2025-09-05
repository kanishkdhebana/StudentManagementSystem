FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

ENV PYTHONPATH=/app
EXPOSE 5001

# CMD ["python3", "./app/app.py"]
CMD ["gunicorn", "app.app:app", "-b", "0.0.0.0:5001"]

