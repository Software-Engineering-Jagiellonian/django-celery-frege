FROM python:3.13
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r ./requirements.txt
COPY download_nltk_data.py download_nltk_data.py
RUN python download_nltk_data.py
COPY . .

