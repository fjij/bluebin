#!/usr/bin/python3.7

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# bluebin.py                                                                  #
#                                                                             #
# Will Harris 2020                                                            #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
import os

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Classes                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class InvalidArgumentException(Exception):
    pass

class IncorrectArgumentCountException(Exception):
    pass

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Functions                                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def parse_args():
    if len(sys.argv) < 3:
        raise IncorrectArgumentCountException('Too few arguments were provided!')
    elif len(sys.argv) > 3:
        raise IncorrectArgumentCountException('Too many arguments were provided!')
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if not os.path.isfile(input_file):
        raise InvalidArgumentException('The input file provided does not exist!')
    return input_file, output_file

def show_help():
    print('\nUsage: python3 bluebin.py [INPUT FILE] [OUTPUT FILE]\n')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Main                                                                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':
    try:
        parse_args()
    except Exception as e:
        print('\nERROR: ' + str(e))
        show_help()


