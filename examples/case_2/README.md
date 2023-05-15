Running the model: Simulation of a large period
===============================================

This example illustrates how to run the model for consecutive time windows in a background year

1. Using a python script where the arguments are defined
2. Using a bash script that iterates through dates and calls python run.py from the terminal
3. Using a bash script that iterates through dates and calls the binary 'pymock' from the terminal

# Python script

The script `ex2_frompy.py` contains the example logic and can be run using any `python` IDE (e.g. spyder, pycharm, etc), if the virtual environment was built already. It can also be run from the terminal as

```shell
python ex2_frompy.py
```
It also contains the figures' generation. Details are found in the script's comments


# A bash script from the terminal 

The script `ex2_fromsh.sh` generates the routine to iterate through multiple days. Just run it as

```
$ bash ex2_fromsh.sh
```

# A bash script using the binary `pymock`

Comment line 25 and uncomment line 26 in the script `ex2_fromsh.sh` which will call the pymock from the command terminal. Then run

```
$ bash ex2_fromsh.sh
```
