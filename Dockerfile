## Install Docker image from trusted source
FROM python:3.8.13

## Setup user args
ARG USERNAME=mockup
ARG USER_UID=1100
ARG USER_GID=$USER_UID
RUN groupadd --non-unique -g $USER_GID $USERNAME \
    && useradd -u $USER_UID -g $USER_GID -s /bin/sh -m $USERNAME

## Set up work directory in the Docker container
WORKDIR /usr/src/mockup/

## Copy the files from the local machine (the repository) to the Docker container
COPY --chown=$USER_UID:$USER_GID . /usr/src/mockup/


## Calls setup.py, install python dependencies and install this model as a python module

ENV VIRTUAL_ENV=/venv/
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -e .

## Docker now will be initialized as user
USER $USERNAME

