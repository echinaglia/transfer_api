FROM matthieugouel/python-gunicorn-nginx:latest

ENV APP_ENVIRONMENT production

COPY requirements.txt /tmp/

RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

COPY . /app
