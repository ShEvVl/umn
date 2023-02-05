FROM python:latest

ENV PYTHONUNBUFFERED 1

ENV LC_ALL=C.UTF-8

ENV LANG=C.UTF-8

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

COPY . /app/

CMD ["python", "run.py"]