# mockup

Mock-up *dummy* model. It serves as template for models competing in the Earthquake Forecasting Experiment
for Italy

## Install in virtual environment

Simply install in a python venv

```
python -m venv venv
source venv/bin/activate
pip install -e .
```

Using Docker is preferred, as described in the following section

## Docker build

Builds the docker container setting permissions for current user (see `Dockerfile`)

```
docker build \
--build-arg USERNAME=$USER \
--build-arg USER_UID=$(id -u) \
--build-arg USER_GID=$(id -g) \
--no-cache \
-t mockup .
```

## Example run

### Simple run using python and parameters.txt

Runs python from the docker image, the model interface (`run.py`), which reads the file `parameters.txt`
(see `run.run_model()`, lines 34-38)

```
docker run --rm --volume $PWD:/usr/src/mockup:rw mockup python run.py
```

### Simple run using binary file and parameters.txt

Runs the model using the binary created from `setup.py`.

```
docker run --rm --volume $PWD:/usr/src/mockup:rw mockup run
```

### Simple run using binary and passing arguments from terminal

Runs the binary using arguments passed from the terminal (preferred way). See function `run.run()` and examples/case_1

```
# docker run --rm --volume ${local_entrypoint}:${image_entrypoint}:${permits} ${image_name} run ${datetime} ${delta_time} ${min_mag}
docker run --rm --volume $PWD:/usr/src/mockup:rw mockup run 2010-01-01 1 4.0
```


