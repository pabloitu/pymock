## Install Docker image from trusted source
FROM python:3.8.13

## Set up work directory in the Docker container
WORKDIR /usr/src/mockup_py

## Copy the files from the local machine (the repository) to the Docker container
COPY . .

## Calls setup.py, install python dependencies and install this model as a python module
RUN pip install -e .

## Creates user "modeler"
RUN groupadd docker && \
    useradd -g docker modeler

## Docker now will be initialized as modeler
USER modeler



