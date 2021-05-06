FROM python:3.9-slim as html_to_pdf
ENV PYTHONUNBUFFERED=1
RUN sed -Ei 's/main$/main contrib/' /etc/apt/sources.list
RUN apt-get update && apt-get install -y git wkhtmltopdf ttf-mscorefonts-installer fonts-bebas-neue default-libmysqlclient-dev
RUN apt-get install -y gcc g++

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN pip install mysqlclient
RUN mkdir /templates

ENV ENVIRONMENT=docker

COPY . /app

WORKDIR /app

#RUN python manage.py makemigrations
#RUN python manage.py migrate
#RUN python manage.py collectstatic --clear --noinput

EXPOSE 8000
