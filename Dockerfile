FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk update

RUN apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir
RUN pip install Django==5.0.1 --no-cache-dir

COPY . .

CMD ["gunicorn", "idp.wsgi:application", "--bind", "0.0.0.0:8000"]
