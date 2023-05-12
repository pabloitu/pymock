Running the model: Simulation of a large period
===================

This example ilustrates how to run the model using multiple ways

1. Using a python script in which the parameters are defined
2. From the terminal using python, passing the model parameters as arguments
3. From the terminal using python, where a parameters.txt file is read
4. From the terminal using an installed binary file

# Python script

The script `ex1_frompy.py` can be run using any `python` IDE (e.g. spyder, pycharm, etc),
given that the virtual environment is setup. Can also be run from the terminal as

```
python ex1_frompy.py
```

Details are found in the script's comments

# From terminal, passing arguments

The script `${pathrepo}/run.py` is the main interface for the model. It has the basic instructions to perform the steps
necessary to create the forecast synthetic catalogs. It could also be placed into the `pymock` folder.
The script can be run from the terminal, by passing the arguments in sequential order,
as stated in the function `run.run_model()`. How arguments are read can be seen in function `run.run()`,
where args are read sequentally from the passed arguments through the terminal (line 55).
For the examples only, we should run the script from each example folder (to access the catalog found there in and save
the forecast), but it is not necessary for the general case.

```
cd examples/case_1

# python ${pathrepo}/run.py datetime delta_time mag_min n_sims seed
python ../../run.py 2010-01-01T00:00:00 1 4.0 10000 23
```

# From terminal, arguments found in parameters.txt

The script `${pathrepo}/run.py`, when no arguments are passed, searches within a parameters.txt found in the
current directory

```
cd examples/case_1

python ../../run.py
```

# From binary

This is the optimal way of running a model. When the model is installed, e.g., from a `setup.py` file, a binary file can
be created and added to the virtual environment path (see `setup.py`, lines 11-13). A similar approach could be the use
of symbolic links, which can be defined within the Dockerfile.

