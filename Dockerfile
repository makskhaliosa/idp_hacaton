FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir
RUN pip install Django==5.0.1 --no-cache-dir

COPY . .

CMD ["gunicorn", "idp.wsgi:application", "--bind", "0.0.0.0:8000"]
