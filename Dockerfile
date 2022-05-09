FROM python:3.8.13

WORKDIR /usr/src/mockup

COPY . .

RUN pip install -e .

RUN groupadd docker && \
    useradd -g docker modeler

USER modeler



