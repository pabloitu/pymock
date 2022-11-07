## Install Docker image from trusted source
FROM python:3.8.13

## Setup user args
ARG USERNAME=pymock         #default. ignored if USERNAME is pased when calling `docker build`
ARG USER_UID=1100           #default
ARG USER_GID=$USER_UID      #default

RUN groupadd --non-unique -g $USER_GID $USERNAME \
    && useradd -u $USER_UID -g $USER_GID -s /bin/sh -m $USERNAME

## Set up work directory in the Docker container. Change {pymock} to {model_name} if this file is used as template
WORKDIR /usr/src/pymock/

## Copy the files explicitly from the local machine (the repository) to the Docker container.
## Change {pymock} to {model_name} if this file is used as template
COPY --chown=$USER_UID:$USER_GID /examples /input /pymock /tests parameters.txt run.py setup.py /usr/src/pymock/


## Calls setup.py, install python dependencies and install this model as a python module

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -e .

## Docker now will be initialized as user
USER $USERNAME

