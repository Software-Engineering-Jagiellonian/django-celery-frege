FROM python:3.13
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt
RUN pip install --no-cache-dir gunicorn==20.1.0
COPY download_nltk_data.py download_nltk_data.py
RUN python download_nltk_data.py
COPY . .

