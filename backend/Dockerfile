FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install pip-tools
COPY requirements.in requirements.in
RUN pip-compile
RUN pip-sync
RUN pip install gunicorn==20.1.0
COPY . .
