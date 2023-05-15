Running the model: Simulation of an unremarkable day
====================================================

This example illustrates how to run the model using multiple ways

1. Using a python script in which the arguments are defined
2. From the terminal using python, passing the model arguments file
3. From the terminal using an installed binary file (requires advanced installation)


# Python script

The script `ex1_frompy.py` contains the example logic and can be run using any `python` IDE (e.g. spyder, pycharm, etc), if the virtual environment was built already. It can also be run from the terminal as

```shell
python ex1_frompy.py
```

It also contains the figures generation. Details are found in the script's comments

# Calling run.py from the rermianl

The script `${pathrepo}/run.py` is the main interface for the model It has the basic instructions to perform the steps
necessary to create the forecast synthetic catalogs.
The arguments file `case_1/inputs/args.txt` can be used for `run.py` from any directory in the terminal. By default, a `forecast` folder will be created in `case_1`


```shell
#from top directory
python run.py examples/case_1/input/args.txt
# or
cd examples/case_1 
python ../../run.py input/args.txt
```


# From the console entry point (advanced)

This is the optimal way of running a model. When the model is installed, e.g., from a `setup.cfg` file, a binary file can
be created and added to the virtual environment path (see `setup.cfg`, lines 28-30).

The entry_point is a command called `pymock` from the terminal and linked to the function `pymock/main.py:run()`. Therefore, we can type

```shell
cd examples/case_1
pymock input/args.txt
```
