Running the model: Simulation of a large period
===============================================

This example illustrates how to run the model for an intense simulation (L'Aquila sequence):

1. Using a python script where the arguments are defined
2. Using a bash script that iterates through dates and calls the binary 'pymock' from the terminal

# Python script

The script `ex3_frompy.py` contains the example logic and can be run using any `python` IDE (e.g. spyder, pycharm, etc), if the virtual environment was built already. It can also be run from the terminal as

```shell
python ex3_frompy.py
```
It also contains the figures' generation. Details are found in the script's comments


# A bash script from the terminal

The script `ex3_fromsh.sh` generates the routine to iterate through multiple days. Just run it as

```
$ bash ex3_fromsh.sh
```
