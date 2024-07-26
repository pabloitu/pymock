import sys
from pymock import main

"""
Run 'wrapper' function.

It receives the input arguments file path (e.g. input/args.txt) from the
command terminal and passes it to the main() function in pymock/main.py.

1. This file can be run from the command terminal as:
   >>> $ python run.py <args_path>
   with default to <args_path> = input/args.txt

2. It can also be run from a python console if needed.

3. (Advanced) An entry_point was defined, so pymock can also be run as:
   >>> $ pymock <args_path>
   * see setup.cfg and pymock.main:run() for details.

"""


def run(default_args='input/args.txt'):

    args = sys.argv  # This reads the arguments given from the terminal

    if len(args) > 2:  # arguments were passed (not supported)
        print('Running using input arguments not supported; provide a path to arguments file')
        exit()

    elif len(args) == 2:  # <args_path> was passed
        print(f'Running using input argument file {args[1]}')
        arg_path = args[1]

    elif len(args) == 1:  # no <args_path> passed, trying default
        print(f'Running using default arguments: {default_args}')
        arg_path = default_args

    try:
        main.main(arg_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arguments file not found at {arg_path}; "
                                "please provide file or a valid path.")


if __name__ == '__main__':
    run()
