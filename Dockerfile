FROM python:latest
COPY requirements.txt .
ENV PYTHONUNBUFFERED=1
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
