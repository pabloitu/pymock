# mockup

Mockup or *dummy* time-dependent model. The repository structure, setup, tests and examples can be used as template for
the models competing in the Earthquake Forecasting
Experiment for Italy.

The model's formulation is the simplest possible, which still captures the code complexity arisen from time-dependency.
It follows a non-homogeneous Poisson process, where the mean rate of events larger than a threhold magnitude
$`m_0`$ is:

```math
\mu(\boldsymbol{x},t, m>m_0) = \hat{\mu}(\boldsymbol{x},m>m_0) + \frac{\displaystyle\int_{t-h}^{t}\lambda(\boldsymbol{x}, \tau, m>m_0)\,\mathrm{d}\tau}{h}
```

where $`\hat{\mu}(\boldsymbol{x}, m>m_0)`$ is the cell's background rate derived from the complete training catalog. The
second term of the right side is the average of the rate $`\lambda`$ obtained from the previous time window of length
$`h`$ (e.g.
1-day).

Stochastic catalogs are drawn from a homogeneous Poisson process, with $`\mu(\boldsymbol{x},t, m>m_0)`$, for a given
time window. Magnitude marks are obtained from a Double-Truncated-GR, with an user-given $`m_{\mathrm{min}}`$ (e.g. 4.0 in the official Italy Experiment)
, and set values of $`b=1`$ and $`m_{\mathrm{max}}=8.0`$.

## Installation

### In a python virtual environment

Install and run using a python venv. In the repository main folder, run:

```
python -m venv venv
source venv/bin/activate
pip install -e .
python run.py
```

To deactivate/reactivate the environment, type `source deactivate`, or `source venv/bin/activate` respectively. (
See `setup.py` and the setup arguments found therein)
Once the code is working in a `python` virtual environment, we suggest the use of Docker, as described in the following
section:

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

This grants Docker Container's read/write permissions to the current local user, along with the instructions
in `Dockerfile`

## Model structure

## Running the model

There are several ways to run the model, for which here a couple are shown. The final choice is left to the modeler
criteria. We suggest running the model as a binary with arguments passed from the terminal.

### Run in Docker, using a parameters.txt file

Runs python from the docker image, the model interface (`run.py`), which reads the file `parameters.txt`
(see `run.run_model()`, lines 34-38)

```
docker run --rm --volume $PWD:/usr/src/mockup:rw mockup python run.py
```


### Run using binary file and parameters.txt

Runs the model using the binary created from `setup.py` (see lines 12-16 therein).

```
docker run --rm --volume $PWD:/usr/src/mockup:rw mockup run
```


### Run using binary and passing arguments from terminal

Runs the binary using arguments passed from the terminal (preferred way). See function `run.run()` and examples/case_1

```
# Code usage
# docker run --rm --volume ${local_entrypoint}:${image_entrypoint}:${permits} ${image_name} run ${datetime} ${delta_time} ${min_mag}
docker run --rm --volume $PWD:/usr/src/mockup:rw mockup run 2010-01-01 1 4.0
```


