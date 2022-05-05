FROM python:3.8.13

WORKDIR /usr/src/mockup

COPY . .

RUN pip install -e .

EXPOSE 5000
