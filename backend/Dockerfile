FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r ./requirements.txt
RUN pip install gunicorn==20.1.0
COPY . .
