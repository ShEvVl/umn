FROM python:3.11.1

WORKDIR /umn

COPY ./requirements.txt /umn/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /umn/

CMD ["python", "run.py"]