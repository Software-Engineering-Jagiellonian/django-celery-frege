FROM python:3.13
ENV PYTHONUNBUFFERED=1
ARG DJANGO_DOWNLOAD_PATH
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY download_nltk_data.py download_nltk_data.py
RUN python download_nltk_data.py
RUN mkdir -p ${DJANGO_DOWNLOAD_PATH}
RUN chown -R nobody:nogroup ${DJANGO_DOWNLOAD_PATH}
COPY . .
