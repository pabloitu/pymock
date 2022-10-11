# mockup

Mockup or *dummy* model, as the repository-structure template for the models competing in the Earthquake Forecasting Experiment for Italy.

The model's formulation is the simplest possible, but still capturing the code complexity arisen due to time-dependency. The model follows a non-homogeneous Poisson process, where the mean rate is:
```math
\mu(t, \boldsymbol{x}) = \hat{\mu}(\boldsymbol{x}) + \cfrac{\int_{t-h}^{t}\lambda(\tau, \boldsymbol{x})\,\mathrm{d}\tau}{h}
```
where $`\hat{\mu}`$ is the background rate obtained from the entire input catalog, and the second term of the right side is simply the average of the rate $\lambda$ in a time window $`h`$ of choice (e.g. 1 day).



## Installation
### In a python virtual environment

Install and run using a python venv. In the repository main folder, run:

```
python -m venv venv
source venv/bin/activate
pip install -e .
python run.py
```

To deactivate/reactivate the environment, type `source deactivate`, or `source venv/bin/activate` respectively. (See `setup.py` and the setup arguments found therein)
Once the code is working in a `python` virtual environment, we suggest the use of Docker, as described in the following section:

### Docker build

Build the docker container:

```
docker build \
--build-arg USERNAME=$USER \
--build-arg USER_UID=$(id -u) \
--build-arg USER_GID=$(id -g) \
--no-cache \
-t mockup .
```
This grants Docker Container's read/write permissions to the current local user, along with the instructions in `Dockerfile`

## Model structure



## Running the model

There are several ways to run the model, for which here a couple are shown. The final choice is left to the modeler criteria. We suggest running the model as a binary with arguments passed from the terminal.

### Run in Docker, using a parameters.txt file

Runs python from the docker image, the model interface (`run.py`), which reads the file `parameters.txt`
(see `run.run_model()`, lines 34-38)

```
docker run --rm --volume $PWD:/usr/src/mockup:rw mockup python run.py
```

### Run using binary file and parameters.txt

Runs the model using the binary created from `setup.py`.

```
docker run --rm --volume $PWD:/usr/src/mockup:rw mockup run
```

### Run using binary and passing arguments from terminal

Runs the binary using arguments passed from the terminal (preferred way). See function `run.run()` and examples/case_1

```
# docker run --rm --volume ${local_entrypoint}:${image_entrypoint}:${permits} ${image_name} run ${datetime} ${delta_time} ${min_mag}
docker run --rm --volume $PWD:/usr/src/mockup:rw mockup run 2010-01-01 1 4.0
```


