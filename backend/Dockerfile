FROM python:3.8
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install libpq-dev gcc build-essential wkhtmltopdf  -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./index /code/index
COPY ./local.py /code/local.py
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]