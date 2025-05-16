# My current python version is 3.13, and psycopg2 model is not support python 3.13 yet, so I edited the setting to 3.11. 
FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y postgresql-client
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
