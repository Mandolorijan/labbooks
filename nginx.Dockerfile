FROM node:18-alpine AS django-npm-builder

WORKDIR /builds
COPY package.json gulpfile.js ./
RUN npm install

FROM python:3.9 AS django-static-builder
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install --no-install-recommends -y cron

WORKDIR /src

COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/nano-bio/fitlib.git@package

COPY ./src .
COPY --from=django-npm-builder /builds/src/_vendor ./_vendor/

RUN python manage.py collectstatic --noinput

FROM nginx:1.23-alpine

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=django-static-builder /src/static /src/static/
